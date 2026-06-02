import csv
import os
from datetime import datetime,timezone

def generate_ebs_report(unused_volumes):

    if not unused_volumes:
        print("No unused EBS volumes found")
        return None

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

    os.makedirs("/tmp/reports_output", exist_ok=True)

    filename = f"/tmp/reports_output/ebs_report_{timestamp}.csv"

    with open(filename, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=unused_volumes[0].keys()
        )

        writer.writeheader()
        writer.writerows(unused_volumes)

    print(f"EBS report saved: {filename}")

    return filename