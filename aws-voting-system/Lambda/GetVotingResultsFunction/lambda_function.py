
import json
import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("VotingSystem")

def lambda_handler(event, context):
    counts = {
        "OptionA": 0,
        "OptionB": 0,
        "OptionC": 0
    }

    response = table.scan(
        ProjectionExpression="VoteOption"
    )

    for item in response.get("Items", []):
        option = item.get("VoteOption")
        if option in counts:
            counts[option] += 1

    while "LastEvaluatedKey" in response:
        response = table.scan(
            ProjectionExpression="VoteOption",
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )

        for item in response.get("Items", []):
            option = item.get("VoteOption")
            if option in counts:
                counts[option] += 1

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "totalVotes": sum(counts.values()),
            "results": counts
        })
    }
