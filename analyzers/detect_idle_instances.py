import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch')

def get_cpu_utilization(instance_id):

    end = datetime.utcnow()
    start = end - timedelta(days=7)

    metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {'Name': 'InstanceId', 'Value': instance_id}
        ],
        StartTime=start,
        EndTime=end,
        Period=3600,
        Statistics=['Average']
    )

    datapoints = metrics['Datapoints']

    if not datapoints:
        return 0

    avg = sum(d['Average'] for d in datapoints) / len(datapoints)
    return avg