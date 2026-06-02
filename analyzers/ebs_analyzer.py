import boto3

ec2 = boto3.client('ec2')

EBS_COST_PER_GB = 0.08

def get_unattached_volumes():
    response = ec2.describe_volumes()
    unused_volumes = []
    for volume in response['Volumes']:
        if not volume['Attachments']:
            size = volume['Size']
            estimated_waste = round(size * EBS_COST_PER_GB, 2)
            unused_volumes.append({
                "VolumeId": volume["VolumeId"],
                "SizeGB": size,
                "State": volume["State"],
                "EstimatedWasteUSD": estimated_waste
            })
    return unused_volumes