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


def get_age_group(entry):
    age_groups = {
        "dragon": [6, 7],
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


def get_belt_group(entry):
    belt_groups = {
        "low": ["white", "yellow", "orange"],
        "middle": ["green", "blue"],
        "high": ["red", "brown"],
        "black": ["black"],
    }
    belt_group = next(
        (group for group, belts in belt_groups.items() if entry["belt"] in belts)
    )

    return belt_group


def set_weight_class(entries):
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


def group_divisions(entries):
    divisions = {}
    sparring_entries = list(
        filter(lambda x: "sparring" in x["events"].split(","), entries)
    )

    for entry in sparring_entries:
        age_group = get_age_group(entry)
        belt_group = get_belt_group(entry)
        key = f"{belt_group}_{age_group}_{entry['gender'][0]}_{entry['weight_class']}"
        if key not in divisions:
            divisions[key] = []
        divisions[key].append(entry)

    return divisions


def generate_division_bracket(entries):
    pairings = []
    while len(entries) >= 2:
        participant1 = entries.pop(0)
        participant2 = entries.pop(0)
        if participant1["school"] == participant2["school"]:
            filtered_entries = [
                p for p in entries if p["school"] != participant1["school"]
            ]
            if len(filtered_entries) > 0:
                participant2 = filtered_entries.pop(0)
        pairings.append((participant1, participant2))

    if len(entries) == 1:
        winner_placeholder = dict(
            name="W1",
            gender=participant1["gender"],
            belt=participant1["belt"],
            age="TBD",
            weight="TBD",
            school="TBD",
        )
        pairings.append((entries[0], winner_placeholder))
    return pairings


def upload_to_s3(entries, filename):
    s3 = boto3.client("s3")
    print(f"Uploading {filename} to {bucket_name}")
    s3.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body=entries,
    )


def main():
    entries = get_current_entries()
    entries = set_weight_class(entries)
    # upload_to_s3(json.dumps(entries, indent=2, default=str), "entries.json")

    divisions = group_divisions(entries)
    for key, value in divisions.items():
        age_group = key.split("_")[1]
        weight_class = key.split("_")[3]
        print(f"Group {key}:")
        bracket = generate_division_bracket(value)
        with open(f"{key}.csv", "w") as out:
            out.write(
                f"#Game Gr.,#Class,#Gender,#Weight,#Chung Name,#Chung Belongs To,#Hong Name,#Hong Belongs To"
            )
            for i, pairing in enumerate(bracket, start=1):
                participant1, participant2 = pairing
                print(f'  Match {i}: {participant1["name"]} vs {participant2["name"]}')

                out.write(
                    f"\n{i},{age_group},{participant1['gender']},{weight_class},{participant1['name']},{participant1['school']},{participant2['name']},{participant2['school']}"
                )


if __name__ == "__main__":
    main()
