from datetime import timezone
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, JSON, Integer, Text, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class FlowtabSource(Base):
    """Configuration for data collection (e.g. Account, Region, VPC)"""
    __tablename__ = "ft_sources"
    
    id = Column(String, primary_key=True)  # {account}:{region}:{vpc}
    account_id = Column(String, nullable=False)
    region = Column(String, nullable=False)
    vpc_id = Column(String, nullable=False)
    name = Column(String)
    mode = Column(String)  # 'demo', 's3'
    settings_json = Column(JSON)  # flow log bucket, eks cluster name, etc.
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
class EniHistory(Base):
    """Tracks ENIs (Elastic Network Interfaces) so deleted resources are known"""
    __tablename__ = "ft_eni_history"
    
    eni_id = Column(String, primary_key=True)
    vpc_id = Column(String, index=True)
    az_id = Column(String)
    account_id = Column(String)
    region = Column(String)
    
    resource_type = Column(String) # 'EC2', 'ELB', 'NAT', 'RDS', 'EKS_NODE'
    resource_id = Column(String)
    name = Column(String)
    private_ip = Column(String, index=True)
    
    first_seen = Column(DateTime)
    last_seen = Column(DateTime)
    
class PodLease(Base):
    """Tracks kubernetes pods IP assignments over time"""
    __tablename__ = "ft_pod_leases"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cluster_name = Column(String, index=True)
    namespace = Column(String)
    workload = Column(String)  # Deployment/DaemonSet/etc name
    pod_name = Column(String)
    pod_ip = Column(String, index=True)
    node_ip = Column(String)
    
    first_seen = Column(DateTime)
    last_seen = Column(DateTime)

class BilledLine(Base):
    """Raw data transfer charge line item from CUR mapped to usage group"""
    __tablename__ = "ft_billed_lines"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    hour = Column(DateTime, index=True)
    account_id = Column(String)
    region = Column(String)
    
    usage_type = Column(String) 
    product_code = Column(String)
    resource_id = Column(String, index=True) # line_item_resource_id
    
    usage_gb = Column(Float)
    cost_usd = Column(Float)

class FlowRecord(Base):
    """Processed aggregate flow log entry allocated with bill data"""
    __tablename__ = "ft_flows"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    hour = Column(DateTime, index=True)
    vpc_id = Column(String, index=True)
    
    sender_type = Column(String)  # 'EC2', 'POD', 'ELB', 'INTERNET', etc.
    sender_id = Column(String)
    sender_name = Column(String)
    
    receiver_type = Column(String)
    receiver_id = Column(String)
    receiver_name = Column(String)
    
    route = Column(String)        # 'intra-vpc', 'internet-egress', 'cross-az', 'cross-region', etc
    charge_category = Column(String)
    
    bytes = Column(Float)
    estimated_usd = Column(Float)
    billed_usd = Column(Float)
    is_estimated = Column(Boolean)
