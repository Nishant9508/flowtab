import time
import boto3
from typing import List, Dict, Any

class AthenaClient:
    def __init__(self, database: str, bucket: str, region: str = "us-east-1"):
        self.database = database
        self.bucket = bucket
        self.client = boto3.client('athena', region_name=region)
        
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        response = self.client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': self.database},
            ResultConfiguration={'OutputLocation': f's3://{self.bucket}/athena-results/'}
        )
        
        execution_id = response['QueryExecutionId']
        
        # Wait for query to complete
        while True:
            status = self.client.get_query_execution(QueryExecutionId=execution_id)
            state = status['QueryExecution']['Status']['State']
            if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            time.sleep(1)
            
        if state != 'SUCCEEDED':
            reason = status['QueryExecution']['Status'].get('StateChangeReason', 'Unknown error')
            raise Exception(f"Athena query failed: {reason}")
            
        results = []
        next_token = None
        
        while True:
            params = {'QueryExecutionId': execution_id}
            if next_token:
                params['NextToken'] = next_token
                
            page = self.client.get_query_results(**params)
            
            # Skip header row if this is the first page
            rows = page['ResultSet']['Rows']
            if not next_token and rows:
                cols = [col.get('VarCharValue', '') for col in rows[0]['Data']]
                rows = rows[1:]
            
            for row in rows:
                values = [col.get('VarCharValue', None) for col in row['Data']]
                results.append(dict(zip(cols, values)))
                
            next_token = page.get('NextToken')
            if not next_token:
                break
                
        return results

def get_athena_client(database: str, bucket: str) -> AthenaClient:
    """Dependency injection friendly accessor"""
    return AthenaClient(database, bucket)
