import os
import json
import boto3
import random


table_name = os.getenv("DB_TABLE")
bucket_name = os.getenv("CONFIG_BUCKET")


def get_current_entries():
    dynamodb = boto3.client("dynamodb")
    items = dynamodb.scan(
        TableName=table_name,
        FilterExpression="reg_type = :competitor",
        ExpressionAttributeValues={
            ":competitor": {
                "S": "competitor",
            },
        },
    )["Items"]
    result = []
    for item in items:
        result.append(
            dict(
                name=item["full_name"]["S"],
                gender=item["gender"]["S"],
                belt=item["beltRank"]["S"],
                age=item["age"]["N"],
                weight=item["weight"]["N"],
                school=item["school"]["S"],
                events=item["events"]["S"],
            )
        )

    return result


def get_coaches():
    dynamodb = boto3.client("dynamodb")
    items = dynamodb.scan(
        TableName=table_name,
        FilterExpression="reg_type = :coach",
        ExpressionAttributeValues={
            ":coach": {
                "S": "coach",
            },
        },
    )["Items"]
    result = []
    for item in items:
        result.append(
            dict(
                name=item["full_name"]["S"],
                school=item["school"]["S"],
            )
        )

    return result


def get_age_group(entry):
    age_groups = {
        "dragon": [5, 6, 7],
        "tiger": [8, 9],
        "youth": [10, 11],
        "cadet": [12, 13, 14],
        "junior": [15, 16],
        "senior": list(range(17, 33)),
        "ultra": list(range(33, 100)),
    }

    age_group = next(
        (group for group, ages in age_groups.items() if int(entry["age"]) in ages)
    )

    return age_group


def set_weight_class(entries):
    s3 = boto3.client("s3")
    weight_classes = json.load(
            s3.get_object(Bucket=bucket_name, Key="weight_classes.json")["Body"]
        )
    updated_entries = []
    for entry in entries:
        age_group = get_age_group(entry)
        weight_class_ranges = weight_classes[age_group][entry["gender"]]
        entry["weight_class"] = next(
            weight_class
            for weight_class, weights in weight_class_ranges.items()
            if float(entry["weight"]) >= float(weights[0])
            and float(entry["weight"]) < float(weights[1])
        )
        updated_entries.append(entry)

    return updated_entries


def upload_to_s3(contents, filename):
    s3 = boto3.client("s3")
    print(f"Uploading {filename} to {bucket_name}")
    s3.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body=contents,
    )


def main():
    entries = get_current_entries()
    entries = set_weight_class(entries)
    upload_to_s3(json.dumps(entries, indent=2, default=str), "entries.json")

    coaches = get_coaches()
    upload_to_s3(json.dumps(coaches, indent=2, default=str), "coaches.json")


if __name__ == "__main__":
    main()
