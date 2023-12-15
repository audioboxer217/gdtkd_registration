import os
import json
import boto3


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


def set_weight_class(entries):
    age_groups = {
        "dragon": [6, 7],
        "tiger": [8, 9],
        "youth": [10, 11],
        "cadet": [12, 13, 14],
        "junior": [15, 16],
        "senior": list(range(17, 33)),
        "ultra": list(range(33, 100)),
    }
    weight_classes = {
        "youth": {
            "male": {"fly": (0, 29.99), "fin": (30, 34.99), "light": (35, 39.99)},
            "female": {"fly": (0, 29.99), "fin": (30, 34.99), "light": (35, 39.99)},
        },
        "cadet": {
            "male": {"fly": (0, 39.99), "fin": (40, 44.99), "light": (45, 49.99)},
            "female": {"fly": (0, 39.99), "fin": (40, 44.99), "light": (45, 49.99)},
        },
    }
    updated_entries = []
    for entry in entries:
        age_group = age_groups[entry["age"]]
        weight_class_ranges = weight_classes[age_group][entry["gender"]]
        for k, v in weight_class_ranges.items():
            if float(entry["weight"]) >= float(v[0]) and float(entry["weight"]) < float(
                v[1]
            ):
                entry["weight_class"] = k
        updated_entries.append(entry)

    return updated_entries


def upload_to_s3(entries):
    s3 = boto3.client("s3")
    print(f"Uploading entries.json to {bucket_name}")
    s3.put_object(
        Bucket=bucket_name,
        Key="entries.json",
        Body=entries,
    )


def main():
    if os.getenv("ENVIRONMENT") == "prod":
        entries = get_current_entries()
    else:
        entries = [
            {
                "name": "Ciin Sing",
                "gender": "female",
                "belt": "black",
                "age": "11",
                "weight": "35.30",
                "school": "GDTKD",
                "events": "sparring,poomsae",
            },
            {
                "name": "Mackenzie Wilson",
                "gender": "female",
                "belt": "brown",
                "age": "11",
                "weight": "31.10",
                "school": "GDTKD",
                "events": "poomsae,breaking,pair poomsae",
            },
            {
                "name": "Jensen Eppler",
                "gender": "female",
                "belt": "black",
                "age": "11",
                "weight": "37.19",
                "school": "GDTKD",
                "events": "sparring,pair poomsae",
            },
            {
                "name": "Jackson Dillingham",
                "gender": "male",
                "belt": "black",
                "age": "13",
                "weight": "47.10",
                "school": "GDTKD",
                "events": "sparring,poomsae",
            },
            {
                "name": "Braden Gile",
                "gender": "male",
                "belt": "black",
                "age": "14",
                "weight": "47.19",
                "school": "GDTKD",
                "events": "sparring,breaking",
            },
            {
                "name": "Lane Grossman",
                "gender": "male",
                "belt": "red",
                "age": "13",
                "weight": "46.50",
                "school": "GDTKD",
                "events": "poomsae,breaking,team poomsae",
            },
        ]

    entries = set_weight_class(entries)
    upload_to_s3(json.dumps(entries, indent=2, default=str))
    # IDEA: if I need to filter by event
    # for event in ["sparring", "poomsae"]:
    #     event_entries = list(filter(lambda x: event in x["events"].split(","), entries))
    #     upload_to_s3(json.dumps(entries, indent=2, default=str), event)


if __name__ == "__main__":
    main()
