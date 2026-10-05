from datetime import timezone
import datetime
from sqlalchemy.orm import Session
from app.models import FlowtabSource, EniHistory, PodLease, BilledLine, FlowRecord

def generate_demo_scenario(db: Session, account_id="demo-123", region="us-east-1", vpc_id="vpc-demo-1"):
    # Clear existing data for this VPC
    db.query(FlowtabSource).filter_by(vpc_id=vpc_id).delete()
    db.query(EniHistory).filter_by(vpc_id=vpc_id).delete()
    db.query(FlowRecord).filter_by(vpc_id=vpc_id).delete()
    
    # 1. Setup Source
    src = FlowtabSource(
        id=f"{account_id}:{region}:{vpc_id}",
        account_id=account_id,
        region=region,
        vpc_id=vpc_id,
        name="Demo VPC",
        mode="demo"
    )
    db.add(src)
    
    # Hour we are simulating: exactly 1 hour ago
    now = datetime.datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    hour = now - datetime.timedelta(hours=1)
    
    # 2. Setup ENIs
    enis = [
        EniHistory(eni_id="eni-nat", vpc_id=vpc_id, account_id=account_id, region=region, az_id=f"{region}a", resource_type="NAT", resource_id="nat-123", name="NAT Gateway A", private_ip="10.0.1.5", first_seen=hour, last_seen=now),
        EniHistory(eni_id="eni-app1", vpc_id=vpc_id, account_id=account_id, region=region, az_id=f"{region}a", resource_type="EKS_NODE", resource_id="i-node1", name="EKS Node A", private_ip="10.0.1.10", first_seen=hour, last_seen=now),
        EniHistory(eni_id="eni-app2", vpc_id=vpc_id, account_id=account_id, region=region, az_id=f"{region}b", resource_type="EKS_NODE", resource_id="i-node2", name="EKS Node B", private_ip="10.0.2.10", first_seen=hour, last_seen=now),
        EniHistory(eni_id="eni-db", vpc_id=vpc_id, account_id=account_id, region=region, az_id=f"{region}b", resource_type="RDS", resource_id="db-master", name="RDS Master database", private_ip="10.0.2.20", first_seen=hour, last_seen=now),
        EniHistory(eni_id="eni-elb", vpc_id=vpc_id, account_id=account_id, region=region, az_id=f"{region}a", resource_type="ELB", resource_id="elb-web", name="Internet facing ALB", private_ip="10.0.1.30", first_seen=hour, last_seen=now)
    ]
    db.add_all(enis)
    db.commit()

    # 3. Setup Pod Leases
    pods = [
        PodLease(cluster_name="demo-cluster", namespace="default", workload="frontend", pod_name="frontend-abcd", pod_ip="10.0.1.50", node_ip="10.0.1.10", first_seen=hour, last_seen=now),
        PodLease(cluster_name="demo-cluster", namespace="backend", workload="api", pod_name="api-xyz", pod_ip="10.0.2.60", node_ip="10.0.2.10", first_seen=hour, last_seen=now)
    ]
    db.add_all(pods)
    db.commit()

    # 4. Synthesize Flows
    # We create mathematically specific flows to test bill allocations later
    # E.g., Cross-AZ from frontend (in AZ-a, pod ip 10.0.1.50) to api (in AZ-b, pod ip 10.0.2.60)
    flows = [
        FlowRecord(hour=hour, vpc_id=vpc_id, sender_type="POD", sender_name="frontend-abcd", receiver_type="POD", receiver_name="api-xyz", route="cross-az", charge_category="Inter-AZ Data Transfer", bytes=10_000_000_000, estimated_usd=0.10, billed_usd=0.08, is_estimated=False),
        FlowRecord(hour=hour, vpc_id=vpc_id, sender_type="POD", sender_name="api-xyz", receiver_type="EC2", receiver_name="RDS Master database", route="intra-az", charge_category="Intra-AZ Data Transfer", bytes=2_000_000_000, estimated_usd=0.0, billed_usd=0.0, is_estimated=False),
        FlowRecord(hour=hour, vpc_id=vpc_id, sender_type="POD", sender_name="api-xyz", receiver_type="INTERNET", receiver_name="External API", route="nat-egress", charge_category="NAT Gateway Data Processing", bytes=5_000_000_000, estimated_usd=0.225, billed_usd=0.225, is_estimated=False),
        FlowRecord(hour=hour, vpc_id=vpc_id, sender_type="INTERNET", sender_name="Public Web", receiver_type="ELB", receiver_name="Internet facing ALB", route="elb-ingress", charge_category="Inbound", bytes=1_000_000_000, estimated_usd=0.0, billed_usd=0.0, is_estimated=False),
        FlowRecord(hour=hour, vpc_id=vpc_id, sender_type="ELB", sender_name="Internet facing ALB", receiver_type="INTERNET", receiver_name="Public Web", route="elb-egress", charge_category="Internet Egress", bytes=15_000_000_000, estimated_usd=1.35, billed_usd=1.35, is_estimated=False),
        FlowRecord(hour=hour, vpc_id=vpc_id, sender_type="POD", sender_name="api-xyz", receiver_type="INTERNET", receiver_name="S3 Public via NAT", route="nat-egress", charge_category="NAT Gateway Data Processing", bytes=50_000_000_000, estimated_usd=2.25, billed_usd=2.25, is_estimated=False),
    ]
    db.add_all(flows)
    db.commit()

