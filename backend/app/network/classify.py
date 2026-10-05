from datetime import datetime, timezone
import json

class FlowClassifier:
    """Takes a raw flow log record and maps it to a Data Transfer category and rate"""
    
    def __init__(self, enis: list, pod_leases: list):
        # We index inventory for O(1) lookups
        self.ip_to_eni = {e.private_ip: e for e in enis if e.private_ip}
        self.pod_ip_to_lease = {p.pod_ip: p for p in pod_leases if p.pod_ip}
        
    def _identify_ip(self, ip: str):
        if not ip: return ("INTERNET", "Unknown", None)
        
        # Check pods first (they sit on top of nodes)
        if ip in self.pod_ip_to_lease:
            return ("POD", self.pod_ip_to_lease[ip].pod_name, self.pod_ip_to_lease[ip])
            
        # Check ENIs
        if ip in self.ip_to_eni:
            eni = self.ip_to_eni[ip]
            return (eni.resource_type, eni.name, eni)
            
        # Is an internal AWS IP?
        if ip.startswith("10.") or ip.startswith("172.") or ip.startswith("192.168."):
            return ("UNKNOWN_INTERNAL", f"Internal IP {ip}", None)
            
        return ("INTERNET", f"Public IP {ip}", None)

    def classify_flow(self, raw_flow: dict) -> dict:
        """
        raw_flow contains vpc-id, srcaddr, dstaddr, bytes, flow-direction, az-id, etc.
        Returns a dictionary suitable for creating a FlowRecord.
        """
        src_ip = raw_flow.get("srcaddr")
        dst_ip = raw_flow.get("dstaddr")
        bytes_tx = float(raw_flow.get("bytes", 0))
        
        sender_type, sender_name, sender_ent = self._identify_ip(src_ip)
        receiver_type, receiver_name, receiver_ent = self._identify_ip(dst_ip)
        
        # Route classification logic
        route = "intra-vpc"
        category = "Intra-VPC Data Transfer (Free)"
        rate = 0.0
        
        # If one end is internet
        if sender_type == "INTERNET" or receiver_type == "INTERNET":
            # Are we going through a NAT?
            if sender_type == "NAT" or receiver_type == "NAT":
                route = "nat-egress"
                category = "NAT Gateway Data Processing"
                rate = 0.045 # Data processing charge per GB + maybe egress
            elif sender_type == "ELB" or receiver_type == "ELB":
                route = "elb-egress"
                category = "Internet Egress"
                rate = 0.09 # Egress charge
            else:
                route = "internet-egress"
                category = "Internet Egress"
                rate = 0.09
                
        # If both are internal, check AZ boundaries
        elif sender_type != "INTERNET" and receiver_type != "INTERNET":
            s_az = sender_ent.az_id if sender_ent and hasattr(sender_ent, 'az_id') else None
            r_az = receiver_ent.az_id if receiver_ent and hasattr(receiver_ent, 'az_id') else None
            
            if s_az and r_az and s_az != r_az:
                route = "cross-az"
                category = "Inter-AZ Data Transfer"
                rate = 0.01
            else:
                route = "intra-az"
                category = "Intra-AZ Data Transfer"
                rate = 0.0
                
        gb = bytes_tx / (1024**3)
        estimated_usd = gb * rate
        
        return {
            "vpc_id": raw_flow.get("vpc_id"),
            "sender_type": sender_type,
            "sender_name": sender_name,
            "receiver_type": receiver_type,
            "receiver_name": receiver_name,
            "route": route,
            "charge_category": category,
            "bytes": bytes_tx,
            "estimated_usd": estimated_usd,
            "billed_usd": 0.0, # Filled in by bill allocation later
            "is_estimated": True
        }
