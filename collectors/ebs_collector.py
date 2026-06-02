import boto3

ec2 = boto3.client('ec2')

def get_unattached_volumes():

    response = ec2.describe_volumes()

    unused = []

    for vol in response['Volumes']:
        if not vol['Attachments']:
            unused.append(vol['VolumeId'])

    return unused
