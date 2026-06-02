import boto3

from cost_explorer import (
    get_service_costs,
    get_total_monthly_cost,
    debug_cost_response
)

ce = boto3.client("ce")

print("\nMonthly Cost")
print(get_total_monthly_cost())

print("\nService Costs")
service_costs = get_service_costs()

for item in service_costs:
    print(item)

print("\nRaw Cost Explorer Response")
print(debug_cost_response())

print("\nCost Explorer Permissions Test")

print(
    ce.get_dimension_values(
        TimePeriod={
            "Start": "2026-05-01",
            "End": "2026-05-31"
        },
        Dimension="SERVICE"
    )
)
sts=boto3.client("sts")
print(sts.get_caller_identity())