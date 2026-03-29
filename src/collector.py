import boto3
from datetime import datetime, timedelta

class AWSCollector:
    def __init__(self):
        self.ce = boto3.client('ce')
        self.ec2 = boto3.client('ec2')
        self.rds = boto3.client('rds')
        self.s3 = boto3.client('s3')

    def get_monthly_spend(self):
        end = datetime.now().date().isoformat()
        start = (datetime.now() - timedelta(days=30)).date().isoformat()
        return self.ce.get_cost_and_usage(
            TimePeriod={'Start': start, 'End': end},
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )

    def get_unattached_volumes(self):
        return self.ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])

    def get_rds_info(self):
        return self.rds.describe_db_instances()['DBInstances']

    def get_s3_waste(self):
        buckets = self.s3.list_buckets()['Buckets']
        missing_policy = []
        for b in buckets:
            try:
                self.s3.get_bucket_lifecycle_configuration(Bucket=b['Name'])
            except:
                missing_policy.append(b['Name'])
        return missing_policy