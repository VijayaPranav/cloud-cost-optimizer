import os

from collectors.ec2_collector import get_instances
from collectors.ebs_collector import get_unattached_volumes
from analyzers.detect_idle_instances import get_cpu_utilization

from reports.generate_ec2_report import generate_ec2_report
from reports.generate_ebs_report import generate_ebs_report

from cloud_storage.s3_uploader import upload_file_to_s3


INSTANCE_COST = {
    "t2.micro": 8,
    "t3.micro": 8,
    "t3.small": 15,
    "t3.medium": 30
}


def run_analysis():

    instances = get_instances()
    print("Instances found:", instances)
    report = []

    for i in instances:

        if i["State"] == "terminated":
            continue

        cpu = get_cpu_utilization(
            i["InstanceId"]
        )

        instance_type = i["InstanceType"]

        estimated_cost = INSTANCE_COST.get(
            instance_type,
            10
        )

        estimated_waste = (
            estimated_cost
            if cpu < 5
            else 0
        )

        recommendation = (
            "Downsize to t3.nano"
            if cpu < 5
            else "No Action"
        )

        potential_savings = (
            estimated_cost * 0.5
            if cpu < 5
            else 0
        )

        report.append({
            "InstanceId": i["InstanceId"],
            "InstanceType": instance_type,
            "CPUUtilization": round(cpu, 2),
            "CPUIdle": cpu < 5,
            "EstimatedWasteUSD": estimated_waste,
            "Recommendation": recommendation,
            "PotentialSavingsUSD": potential_savings
        })

    unused_volumes = get_unattached_volumes()
   
    ec2_report_file = generate_ec2_report(report)
    print("EC2 report file:", ec2_report_file)

    if ec2_report_file:
        upload_file_to_s3(
        ec2_report_file,
        f"ec2-reports/{os.path.basename(ec2_report_file)}"
    )

    ebs_report_file = generate_ebs_report(
    unused_volumes
    )

    if ebs_report_file:
        upload_file_to_s3(
        ebs_report_file,
        f"ebs-reports/{os.path.basename(ebs_report_file)}"
    )

    return {
        "status": "success",
        "ec2_instances": len(report),
        "unused_ebs": len(unused_volumes)
    }