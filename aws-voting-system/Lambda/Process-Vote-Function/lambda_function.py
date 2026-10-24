
import json
import boto3
import uuid
from datetime import datetime, timezone
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("VotingSystem")

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST",
    "Content-Type": "application/json"
}

def response(status, data):
    return {
        "statusCode": status,
        "headers": headers,
        "body": json.dumps(data)
    }

def lambda_handler(event, context):
    try:
        body = event

        if "body" in event:
            if isinstance(event["body"], str):
                body = json.loads(event["body"])
            elif isinstance(event["body"], dict):
                body = event["body"]

        vote_option = body.get("voteOption")

        if not vote_option:
            return response(400, {
                "message": "Missing voteOption. Provide a voting option."
            })

        vote_id = str(uuid.uuid4())

        table.put_item(
            Item={
                "VoteID": vote_id,
                "VoteOption": str(vote_option),
                "CreatedAt": datetime.now(timezone.utc).isoformat()
            }
        )

        return response(200, {
            "message": "Vote recorded successfully",
            "voteId": vote_id,
            "voteOption": str(vote_option)
        })

    except ClientError as e:
        return response(500, {
            "message": "DynamoDB error",
            "error": e.response["Error"]["Message"]
        })

    except Exception as e:
        return response(500, {
            "message": "Unexpected error",
            "error": str(e)
        })
