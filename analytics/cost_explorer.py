import boto3
from datetime import date,timedelta

ce = boto3.client("ce")
def get_time_period():

    today = date.today()

    start_date = today.replace(day=1)

    end_date = today + timedelta(days=1)

    return {
        "Start": start_date.strftime("%Y-%m-%d"),
        "End": end_date.strftime("%Y-%m-%d")
    }

def get_service_costs():

    response = ce.get_cost_and_usage(
        TimePeriod=get_time_period(),
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[
            {
                "Type": "DIMENSION",
                "Key": "SERVICE"
            }
        ]
    )

    service_costs = []

    for group in response["ResultsByTime"][0]["Groups"]:

        service_name = group["Keys"][0]

        amount = float(
            group["Metrics"]["UnblendedCost"]["Amount"]
        )

        service_costs.append({
            "Service": service_name,
            "CostUSD": round(amount, 4)
        })

    return service_costs

def get_total_monthly_cost():

    response = ce.get_cost_and_usage(
        TimePeriod=get_time_period(),
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"]
    )
    amount = float(
        response["ResultsByTime"][0]
        ["Total"]["UnblendedCost"]
        ["Amount"]
    )
    if abs(amount) < 0.01:
        return 0

    return round(amount, 2)

def debug_cost_response():

    today = date.today()

    response = ce.get_cost_and_usage(
        TimePeriod={
            "Start": today.replace(day=1).strftime("%Y-%m-%d"),
            "End": today.strftime("%Y-%m-%d")
        },
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[
            {
                "Type": "DIMENSION",
                "Key": "SERVICE"
            }
        ]
    )

    return response