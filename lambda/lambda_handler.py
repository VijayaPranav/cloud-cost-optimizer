from analyzer import run_analysis

def lambda_handler(event, context):

    result = run_analysis()

    return {
        "statusCode": 200,
        "body": result
    }