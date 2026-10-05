import random
import datetime
from datetime import timezone, timedelta
from sqlalchemy.orm import Session
from app.models import FlowtabSource, EniHistory, PodLease, BilledLine, FlowRecord

def generate_demo_scenario(db: Session, account_id=None, region=None, vpc_id=None):
    random.seed(42)
    
    # Clear existing
    db.query(FlowtabSource).delete()
    db.query(EniHistory).delete()
    db.query(PodLease).delete()
    db.query(BilledLine).delete()
    db.query(FlowRecord).delete()
    
    accounts = ["111111111111", "222222222222"]
    regions = ["us-east-2", "ap-south-1"]
    vpcs = [
        {"id": "vpc-a1", "acc": accounts[0], "reg": regions[0], "name": "Prod EKS"},
        {"id": "vpc-a2", "acc": accounts[0], "reg": regions[0], "name": "Prod Data"},
        {"id": "vpc-b1", "acc": accounts[1], "reg": regions[1], "name": "DR Data"}
    ]
    
    for v in vpcs:
        db.add(FlowtabSource(
            id=f"{v['acc']}:{v['reg']}:{v['id']}",
            account_id=v['acc'], region=v['reg'], vpc_id=v['id'],
            name=v['name'], mode="demo"
        ))
        
    now = datetime.datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    start_time = now - timedelta(hours=168)
    
    # Create static ENIs and Pods...
    # EKS in vpc-a1
    services = ["gateway", "auth", "inventory", "workers", "reports"]
    for i in range(12):
        svc = services[i % len(services)]
        db.add(PodLease(
            cluster_name="eks-prod", namespace="default", workload=svc,
            pod_name=f"{svc}-pod-{i}", pod_ip=f"10.0.1.{50+i}", node_ip=f"10.0.1.10",
            first_seen=start_time, last_seen=now
        ))

    db.commit()

    # Egress NAT in vpc-a1
    db.add(EniHistory(eni_id="eni-nat", vpc_id="vpc-a1", account_id=accounts[0], region=regions[0], az_id="us-east-2a", resource_type="NAT", resource_id="nat-123", name="NAT Gateway", private_ip="10.0.1.5", first_seen=start_time, last_seen=now))
    db.add(EniHistory(eni_id="eni-alb", vpc_id="vpc-a1", account_id=accounts[0], region=regions[0], az_id="us-east-2b", resource_type="ELB", resource_id="alb-pub", name="Public ALB", private_ip="10.0.1.6", first_seen=start_time, last_seen=now))
    db.add(EniHistory(eni_id="eni-rds-us", vpc_id="vpc-a2", account_id=accounts[0], region=regions[0], az_id="us-east-2a", resource_type="RDS", resource_id="rds-master", name="RDS Master", private_ip="10.0.2.10", first_seen=start_time, last_seen=now))
    db.add(EniHistory(eni_id="eni-rds-ap", vpc_id="vpc-b1", account_id=accounts[1], region=regions[1], az_id="ap-south-1a", resource_type="RDS", resource_id="rds-replica", name="RDS Replica", private_ip="10.0.3.10", first_seen=start_time, last_seen=now))
    db.commit()

    total_s3_nat_bytes = 0
    total_chatty_bytes = 0
    total_peering_bytes = 0
    total_alb_actual_bytes = 0

    GB = 1024**3
    rates = {
        "nat-processing": 0.045, # per GB
        "cross-az": 0.01,
        "cross-region": 0.02, # simplified
        "internet": 0.09
    }
    
    for h in range(168):
        hour = start_time + timedelta(hours=h)
        is_estimated = (168 - h) <= 6
        
        flows = []
        bills = []
        
        # a) Huge S3 out over NAT (vpc-a1)
        # ~200 GB/hr
        s3_bytes = 200 * GB + random.randint(-5*GB, 5*GB)
        total_s3_nat_bytes += s3_bytes
        c_s3 = (s3_bytes / GB) * rates["nat-processing"]
        flows.append(FlowRecord(hour=hour, vpc_id="vpc-a1", sender_type="POD", sender_name="reports-pod-4", receiver_type="INTERNET", receiver_name="S3 via NAT", route="nat-egress", charge_category="NAT Gateway Data Processing", bytes=s3_bytes, estimated_usd=c_s3, billed_usd=c_s3 if not is_estimated else None, is_estimated=is_estimated))
        if not is_estimated:
            bills.append(BilledLine(hour=hour, account_id=accounts[0], region=regions[0], usage_type="NatGateway-Bytes", product_code="AmazonEC2", resource_id="nat-123", usage_gb=s3_bytes/GB, cost_usd=c_s3))
            
        # b) Chatty Cross-AZ
        chatty_bytes = 50 * GB + random.randint(-2*GB, 2*GB)
        total_chatty_bytes += chatty_bytes
        c_chatty = (chatty_bytes / GB) * rates["cross-az"]
        flows.append(FlowRecord(hour=hour, vpc_id="vpc-a1", sender_type="POD", sender_name="gateway-pod-0", receiver_type="POD", receiver_name="auth-pod-1", route="cross-az", charge_category="Inter-AZ Data Transfer", bytes=chatty_bytes, estimated_usd=c_chatty, billed_usd=c_chatty if not is_estimated else None, is_estimated=is_estimated))
        if not is_estimated:
            bills.append(BilledLine(hour=hour, account_id=accounts[0], region=regions[0], usage_type="DataTransfer-Regional-Bytes", product_code="AmazonEC2", resource_id="i-node1", usage_gb=chatty_bytes/GB, cost_usd=c_chatty))

        # c) Region Peering Replication
        peer_bytes = 10 * GB
        total_peering_bytes += peer_bytes
        c_peer = (peer_bytes / GB) * rates["cross-region"]
        flows.append(FlowRecord(hour=hour, vpc_id="vpc-a2", sender_type="EC2", sender_name="RDS Master", receiver_type="EC2", receiver_name="RDS Replica", route="cross-region", charge_category="Inter-Region Data Transfer", bytes=peer_bytes, estimated_usd=c_peer, billed_usd=c_peer if not is_estimated else None, is_estimated=is_estimated))
        if not is_estimated:
            bills.append(BilledLine(hour=hour, account_id=accounts[0], region=regions[0], usage_type="DataTransfer-Out-Bytes", product_code="AmazonEC2", resource_id="rds-master", usage_gb=peer_bytes/GB, cost_usd=c_peer))

        # d) Legitimate ALB Egress (miss-counted by flow logs)
        # Flow logs see 50 GB. Reality is 50 / 0.56 = 89.28 GB
        alb_flow_bytes = 50 * GB
        alb_real_bytes = int(alb_flow_bytes / 0.56)
        total_alb_actual_bytes += alb_real_bytes
        c_alb_est = (alb_flow_bytes / GB) * rates["internet"]
        c_alb_real = (alb_real_bytes / GB) * rates["internet"]
        
        flows.append(FlowRecord(hour=hour, vpc_id="vpc-a1", sender_type="ELB", sender_name="Public ALB", receiver_type="INTERNET", receiver_name="Public Web", route="elb-egress", charge_category="Internet Egress", bytes=alb_flow_bytes, estimated_usd=c_alb_est, billed_usd=c_alb_real if not is_estimated else None, is_estimated=is_estimated))
        if not is_estimated:
            bills.append(BilledLine(hour=hour, account_id=accounts[0], region=regions[0], usage_type="DataTransfer-Out-Bytes", product_code="AmazonEC2", resource_id="alb-pub", usage_gb=alb_real_bytes/GB, cost_usd=c_alb_real))

        # e) Spike on day 6 (hours 120-144)
        if 120 <= h < 144:
            spike_bytes = 500 * GB
            c_spike = (spike_bytes / GB) * rates["internet"]
            flows.append(FlowRecord(hour=hour, vpc_id="vpc-a1", sender_type="POD", sender_name="workers-pod-3", receiver_type="INTERNET", receiver_name="Unknown IP", route="internet-egress", charge_category="Internet Egress", bytes=spike_bytes, estimated_usd=c_spike, billed_usd=c_spike if not is_estimated else None, is_estimated=is_estimated))
            if not is_estimated:
                bills.append(BilledLine(hour=hour, account_id=accounts[0], region=regions[0], usage_type="DataTransfer-Out-Bytes", product_code="AmazonEC2", resource_id="nat-123", usage_gb=spike_bytes/GB, cost_usd=c_spike))

        db.add_all(flows)
        db.add_all(bills)
        
    db.commit()
    
    # Store documentation of test facts
    import os
    docs_path = os.path.join(os.path.dirname(__file__), "../../../docs/DEMO_STORIES.md")

    # Try to write if running locally, otherwise skip
    try:
        with open(docs_path, "w") as f:
            f.write(f"# Demo Scenario Totals\n\nBase values over 7 days:\n")
            f.write(f"- S3 over NAT approx: ${(total_s3_nat_bytes/GB)*rates['nat-processing']:.2f}\n")
            f.write(f"- Chatty app cross AZ: ${(total_chatty_bytes/GB)*rates['cross-az']:.2f}\n")
            f.write(f"- Replication peering: ${(total_peering_bytes/GB)*rates['cross-region']:.2f}\n")
            f.write(f"- ALB true outbound (with 44% undercount on flow side): ${(total_alb_actual_bytes/GB)*rates['internet']:.2f}\n")
            f.write(f"- Spike Day 6: ${(500 * 24)*rates['internet']:.2f}\n")
    except Exception:
        pass
