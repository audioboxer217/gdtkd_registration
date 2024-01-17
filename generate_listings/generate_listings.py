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
    full_brackets = len(entries) & (len(entries) - 1)
    if full_brackets == 0:
        full_brackets = len(entries)
        addl_matches = 0
    else:
        addl_matches = len(entries) - full_brackets

    random.shuffle(entries)  # Shuffle entries for random pairings
    while len(entries) > addl_matches:
        current_entry = entries.pop()

        for i, entry in enumerate(entries):
            if entry["school"] != current_entry["school"]:
                pairings.append((current_entry, entries.pop(i)))
                break

    for i, entry in enumerate(entries):
        winner_placeholder = dict(
            name=f"W{i+1}",
            gender=pairings[0][0]["gender"],
            belt=pairings[0][0]["belt"],
            age="TBD",
            weight="TBD",
            school="TBD",
        )
        pairings.append((entries.pop(i), winner_placeholder))
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
    upload_to_s3(json.dumps(entries, indent=2, default=str), "entries.json")

    coaches = get_coaches()
    upload_to_s3(json.dumps(coaches, indent=2, default=str), "coaches.json")

    divisions = group_divisions(entries)
    single_entry_div = []
    for key, value in divisions.items():
        age_group = key.split("_")[1]
        weight_class = key.split("_")[3]
        print(f"Group {key}:")
        if len(value) == 1:
            single_entry_div.append(value[0])
            print(f"Single competitor {value[0]['name']} added to exhibition list.")
        else:
            bracket = generate_division_bracket(value)
            with open(f"{key}.csv", "w") as out:
                out.write(
                    f"#Game Gr.,#Class,#Gender,#Weight,#Chung Name,#Chung Belongs To,#Hong Name,#Hong Belongs To"
                )
                for i, pairing in enumerate(bracket, start=1):
                    participant1, participant2 = pairing
                    print(
                        f'  Match {i}: {participant1["name"]} ({participant1["school"]}) vs {participant2["name"]} ({participant2["school"]})'
                    )

                    out.write(
                        f"\n{i},{age_group},{participant1['gender']},{weight_class},{participant1['name']},{participant1['school']},{participant2['name']},{participant2['school']}"
                    )

    with open("exhibition_entries.csv", "w") as out:
        out.write("name,belt,age,gender,weight,weight_class,school")
        for entry in single_entry_div:
            out.write(
                f"\n{entry['name']},{entry['belt']},{entry['age']},{entry['gender']},{entry['weight']},{entry['weight_class']},{participant1['school']}"
            )


if __name__ == "__main__":
    main()
