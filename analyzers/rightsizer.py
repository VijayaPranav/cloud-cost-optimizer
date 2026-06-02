INSTANCE_PRICING = {
    "t3.nano": 4,
    "t3.micro": 8,
    "t3.small": 15,
    "t3.medium": 30
}


def get_rightsizing_recommendation(instance_type, cpu):

    if cpu < 5:

        if instance_type == "t3.micro":
            return {
                "Recommendation": "Downsize to t3.nano",
                "PotentialSavingsUSD": 4
            }

        elif instance_type == "t3.small":
            return {
                "Recommendation": "Downsize to t3.micro",
                "PotentialSavingsUSD": 7
            }

        elif instance_type == "t3.medium":
            return {
                "Recommendation": "Downsize to t3.small",
                "PotentialSavingsUSD": 15
            }

        else:
            return {
                "Recommendation": "Consider stopping instance",
                "PotentialSavingsUSD": 0
            }

    elif cpu < 20:

        return {
            "Recommendation": "Consider downsizing",
            "PotentialSavingsUSD": 0
        }

    else:

        return {
            "Recommendation": "Instance appropriately sized",
            "PotentialSavingsUSD": 0
        }