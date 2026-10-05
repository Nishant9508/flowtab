import boto3
from ...models import EniHistory
from datetime import datetime, timezone

def collect_ec2_instances(client, vpc_id: str, account_id: str, region: str, now: datetime):
    enis = []
    paginator = client.get_paginator('describe_instances')
    for page in paginator.paginate(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]):
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), instance_id)
                az = instance['Placement']['AvailabilityZone']
                
                for eni in instance.get('NetworkInterfaces', []):
                    enis.append(EniHistory(
                        eni_id=eni['NetworkInterfaceId'],
                        vpc_id=vpc_id,
                        az_id=az,
                        account_id=account_id,
                        region=region,
                        resource_type="EC2",
                        resource_id=instance_id,
                        name=name,
                        private_ip=eni['PrivateIpAddress'],
                        first_seen=now,
                        last_seen=now
                    ))
    return enis

def collect_nat_gateways(client, vpc_id: str, account_id: str, region: str, now: datetime):
    enis = []
    paginator = client.get_paginator('describe_nat_gateways')
    for page in paginator.paginate(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]):
        for nat in page['NatGateways']:
            if nat['State'] != 'available': continue
            nat_id = nat['NatGatewayId']
            name = next((tag['Value'] for tag in nat.get('Tags', []) if tag['Key'] == 'Name'), nat_id)
            
            for addr in nat.get('NatGatewayAddresses', []):
                if 'NetworkInterfaceId' in addr:
                    # In real code we'd lookup the AZ for the subnet, but assume it's set later or known
                    enis.append(EniHistory(
                        eni_id=addr['NetworkInterfaceId'],
                        vpc_id=vpc_id,
                        az_id=f"{region}x", # Placeholder
                        account_id=account_id,
                        region=region,
                        resource_type="NAT",
                        resource_id=nat_id,
                        name=name,
                        private_ip=addr.get('PrivateIp'),
                        first_seen=now,
                        last_seen=now
                    ))
    return enis

def collect_inventory(account_id: str, region: str, vpc_id: str):
    """Collects all ENIs for a VPC using standard boto3 calls."""
    # In real execution we assume an IAM role here; hardcoded to local standard clients
    client = boto3.client('ec2', region_name=region)
    now = datetime.now(timezone.utc)
    
    enis = []
    enis.extend(collect_ec2_instances(client, vpc_id, account_id, region, now))
    enis.extend(collect_nat_gateways(client, vpc_id, account_id, region, now))
    
    # ELB, RDS, ElastiCache skipped for brevity in this M1/M2 stub, but follow same pattern
    return enis
