import matplotlib.pyplot as plt
#graph for ec2 usage
def plot_cpu_usage(report):
    instance_ids = [r["InstanceId"] for r in report]

    cpu_values = [r["CPUUtilization"] for r in report]

    colors = ["red" if r["CPUIdle"] else "green"for r in report]

    plt.figure(figsize=(10,5))
    plt.bar(instance_ids, cpu_values, color=colors)
    plt.xlabel("Instance ID")
    plt.ylabel("CPU Usage (%)")
    plt.title("EC2 CPU Utilization")
    plt.xticks(rotation=0)#change at last 
  
    plt.axhline(y=5,color='black',linestyle='--',label='Idle Threshold (5%)')

    for i, v in enumerate(cpu_values):
        plt.text(i,v + 0.2,f"{v}%",ha='center')

    plt.legend()
    plt.tight_layout()
    plt.show()
#graph for wastage vs usage of instances
def plot_waste_cost(report):
    instance_ids = [r["InstanceId"] for r in report]
    waste = [r["EstimatedWasteUSD"] for r in report]
    colors = ["red" if w > 0 else "green"for w in waste]

    plt.figure(figsize=(10,5))
    plt.bar(instance_ids, waste, color=colors)
    plt.xlabel("Instance ID")
    plt.ylabel("Estimated Waste ($)")
    plt.title("Estimated Monthly Cost Waste")
    # Threshold line
    plt.axhline(y=0,color='black',linestyle='--',label='No Waste Threshold'
    )

    for i, v in enumerate(waste):
        plt.text(i,v + 0.2,f"${v}",ha='center')

    plt.legend()
    plt.tight_layout()
    plt.show()
#graph for ebs wastage
def plot_ebs_waste(unused_volumes):
    volume_ids = [v["VolumeId"] for v in unused_volumes]
    waste = [v["EstimatedWasteUSD"] for v in unused_volumes]
    colors = ["orange" if w > 0 else "blue"for w in waste]

    plt.figure(figsize=(10,5))
    plt.bar(volume_ids, waste, color=colors)
    plt.xlabel("Volume ID")
    plt.ylabel("Estimated Waste ($)")
    plt.title("Unused EBS Volume Waste")
    plt.axhline(y=0,color='black',linestyle='--',label='No Waste Threshold')
    for i, v in enumerate(waste):
        plt.text(i,v + 0.2,f"${v}",ha='center')

    plt.legend()
    plt.tight_layout()
    plt.show()

