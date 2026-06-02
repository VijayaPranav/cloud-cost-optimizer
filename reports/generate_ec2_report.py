import csv
import os
from datetime import datetime,timezone

def generate_ec2_report(report):

    if not report:
        print("No EC2 data found")
        return None

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

    os.makedirs("/tmp/reports_output", exist_ok=True)

    filename = f"/tmp/reports_output/ec2_report_{timestamp}.csv"

    with open(filename, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=report[0].keys()
        )

        writer.writeheader()
        writer.writerows(report)

    print(f"EC2 report saved: {filename}")

    return filename