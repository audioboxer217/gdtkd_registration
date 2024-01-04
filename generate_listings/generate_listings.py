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
        "dragon": {
            "male": {
                "fin": (0, 18.99),
                "light": (19, 22.99),
                "middle": (23, 26.99),
                "heavy": (27, 50),
            },
            "female": {
                "fin": (0, 18.99),
                "light": (19, 22.99),
                "middle": (23, 26.99),
                "heavy": (27, 50),
            },
        },
        "tiger": {
            "male": {
                "fin": (0, 20.99),
                "light": (21, 24.99),
                "middle": (25, 29.99),
                "heavy": (30, 50),
            },
            "female": {
                "fin": (0, 20.99),
                "light": (21, 24.99),
                "middle": (25, 29.99),
                "heavy": (30, 50),
            },
        },
        "youth": {
            "male": {
                "fin": (0, 29.99),
                "light": (30, 34.99),
                "middle": (35, 39.99),
                "heavy": (40, 99),
            },
            "female": {
                "fin": (0, 29.99),
                "light": (30, 34.99),
                "middle": (35, 39.99),
                "heavy": (40, 99),
            },
        },
        "cadet": {
            "male": {
                "fin": (0, 32.99),
                "fly": (33, 36.99),
                "bantham": (37, 40.99),
                "feather": (41, 44.99),
                "light": (45, 48.99),
                "welter": (49, 52.99),
                "light middle": (53, 56.99),
                "middle": (57, 60.99),
                "light heavy": (61, 64.99),
                "heavy": (65, 99),
            },
            "female": {
                "fin": (0, 28.99),
                "fly": (29, 32.99),
                "bantham": (33, 36.99),
                "feather": (37, 40.99),
                "light": (41, 43.99),
                "welter": (44, 46.99),
                "light middle": (47, 50.99),
                "middle": (51, 54.99),
                "light heavy": (55, 58.99),
                "heavy": (59, 99),
            },
        },
        "junior": {
            "male": {
                "fin": (0, 44.99),
                "fly": (45, 47.99),
                "bantham": (48, 50.99),
                "feather": (51, 54.99),
                "light": (55, 58.99),
                "welter": (59, 62.99),
                "light middle": (63, 67.99),
                "middle": (68, 72.99),
                "light heavy": (73, 77.99),
                "heavy": (78, 99),
            },
            "female": {
                "fin": (0, 41.99),
                "fly": (42, 43.99),
                "bantham": (44, 45.99),
                "feather": (46, 48.99),
                "light": (49, 50.99),
                "welter": (52, 54.99),
                "light middle": (55, 58.99),
                "middle": (59, 62.99),
                "light heavy": (63, 67.99),
                "heavy": (68, 99),
            },
        },
        "senior": {
            "male": {
                "fin": (0, 53.99),
                "fly": (54, 57.99),
                "bantham": (58, 62.99),
                "feather": (63, 67.99),
                "light": (68, 73.99),
                "welter": (74, 79.99),
                "middle": (80, 86.99),
                "heavy": (87, 199),
            },
            "female": {
                "fin": (0, 45.99),
                "fly": (46, 48.99),
                "bantham": (49, 52.99),
                "feather": (53, 56.99),
                "light": (57, 61.99),
                "welter": (62, 66.99),
                "middle": (67, 72.99),
                "heavy": (73, 199),
            },
        },
        "ultra": {
            "male": {
                "fin": (0, 57.99),
                "light": (58, 67.99),
                "middle": (68, 79.99),
                "heavy": (80, 199),
            },
            "female": {
                "fin": (0, 48.99),
                "light": (49, 56.99),
                "middle": (57, 66.99),
                "heavy": (67, 50),
            },
        },
    }
    updated_entries = []
    for entry in entries:
        age_group = next(
            (group for group, ages in age_groups.items() if int(entry["age"]) in ages)
        )
        weight_class_ranges = weight_classes[age_group][entry["gender"]]
        entry["weight_class"] = next(
            weight_class
            for weight_class, weights in weight_class_ranges.items()
            if float(entry["weight"]) >= float(weights[0])
            and float(entry["weight"]) < float(weights[1])
        )
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
