import boto3

ec2 = boto3.client("ec2")


def get_instances():

    response = ec2.describe_instances()

    instances = []

    for reservation in response["Reservations"]:

        for instance in reservation["Instances"]:

            instances.append({

                "InstanceId":
                    instance["InstanceId"],

                "InstanceType":
                    instance["InstanceType"],

                "State":
                    instance["State"]["Name"]
            })

    return instances