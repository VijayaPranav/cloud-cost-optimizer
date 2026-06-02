import subprocess
import os
from collectors.ec2_collector import get_instances
from analyzers.detect_idle_instances import (
    get_cpu_utilization
)
from collectors.ebs_collector import (
    get_unattached_volumes
)
from reports.generate_ec2_report import (
    generate_ec2_report
)
from reports.generate_ebs_report import (
    generate_ebs_report
 )
from cloud_storage.s3_uploader import (
        upload_file_to_s3
)
from analyzers.rightsizer import get_rightsizing_recommendation

# INSTANCE COST MAP
INSTANCE_COST = {
    "t2.micro": 8,
    "t3.micro": 8,
    "t3.small": 15,
    "t3.medium": 30
}

# EC2 ANALYSIS
instances = get_instances()
print(instances)
report = []
for i in instances:    
    if i["State"] != "running":
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
        get_rightsizing_recommendation(
            instance_type,
            cpu
        )
    )
    report.append({
        "InstanceId":
            i["InstanceId"],
        "InstanceType":
            instance_type,
        "CPUUtilization":
            round(cpu, 2),
        "CPUIdle":
            cpu < 5,
        "EstimatedWasteUSD":
            estimated_waste,
        "Recommendation":
            recommendation["Recommendation"],
        "PotentialSavingsUSD":
            recommendation[
                "PotentialSavingsUSD"
            ]
    })
# EBS ANALYSIS
unused_volumes = get_unattached_volumes()

# COST SUMMARY
total_waste = sum(
    r["EstimatedWasteUSD"]
    for r in report
)
total_ebs_waste = sum(
    v["EstimatedWasteUSD"]
    for v in unused_volumes
)
grand_total = (
    total_waste
    + total_ebs_waste
)
print("\nCloud Cost Summary\n")
print(
    f"Total EC2 Waste: ${total_waste}"
)
print(
    f"Total EBS Waste: ${total_ebs_waste}"
)
print(
    f"Total Estimated Cloud Waste: ${grand_total}"
)
    # GENERATE REPORTS
'''print("\nREPORT CONTENTS:")
print(report)

print("\nREPORT LENGTH:")
print(len(report))'''
ec2_report_file = generate_ec2_report(
    report
)
ebs_report_file = generate_ebs_report(
    unused_volumes
)
# UPLOAD REPORTS TO S3
upload_file_to_s3(
    ec2_report_file,
    f"ec2-reports/{os.path.basename(ec2_report_file)}"
)
if ebs_report_file:
    upload_file_to_s3(
    ebs_report_file,
    f"ebs-reports/{os.path.basename(ebs_report_file)}"
    )
#Recommendation page

# LAUNCH STREAMLIT DASHBOARD
print("\nLaunching Streamlit Dashboard...\n")
subprocess.run(
    ["streamlit","run","dashboard.py"]
)











