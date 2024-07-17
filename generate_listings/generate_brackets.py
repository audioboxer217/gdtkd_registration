import os
import json
import boto3
import asyncio
import challonge

table_name = os.getenv("DB_TABLE")
bucket_name = os.getenv("CONFIG_BUCKET")
competition_name = os.getenv("COMPETITION_NAME").replace(" ","_")

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


def get_belt_group(entry):
    belt_groups = {
        "low": ["white", "yellow", "orange"],
        "middle": ["green", "blue"],
        "high": ["red", "brown"],
        "black": ["black", "1 black", "2 black", "3 black", "master black"],
    }
    belt_group = next(
        (group for group, belts in belt_groups.items() if entry["belt"] in belts)
    )

    return belt_group


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

    sparring_gr_entries = list(
        filter(lambda x: "sparring-gr" in x["events"].split(","), entries)
    )
    for entry in sparring_gr_entries:
        age_group = get_age_group(entry)
        belt_group = get_belt_group(entry)
        key = (
            f"{belt_group}-gr_{age_group}_{entry['gender'][0]}_{entry['weight_class']}"
        )
        if key not in divisions:
            divisions[key] = []
        divisions[key].append(entry)

    sparring_wc_entries = list(
        filter(lambda x: "sparring-wc" in x["events"].split(","), entries)
    )
    for entry in sparring_wc_entries:
        age_group = get_age_group(entry)
        belt_group = get_belt_group(entry)
        key = (
            f"{belt_group}-wc_{age_group}_{entry['gender'][0]}_{entry['weight_class']}"
        )
        if key not in divisions:
            divisions[key] = []
        divisions[key].append(entry)

    return divisions


async def generate_division_bracket(division, entries):
    entries = sorted(entries, key=lambda d: d['school'])

    c = await challonge.get_user(os.getenv("CHALLONGE_USERNAME"), os.getenv("CHALLONGE_PASSWORD"))
    tournament = await c.create_tournament(
        name = f"{competition_name}_{division}",
        url = f"{competition_name}_{division.replace(' ','_').replace('-','_')}",
    )

    for e in entries:
        await tournament.add_participant(display_name=e['name'], misc=e['school'])
    
    await tournament.start()

    return tournament


async def get_match_details(bracket):
    matches = await bracket.get_matches()

    pairings = []
    for match in matches:
        if match.round == 1:
            participant1 = await bracket.get_participant(match.player1_id)
            participant2 = await bracket.get_participant(match.player2_id)

        if match.round == 2:
            if match.player1_id is not None:
                participant1 = await bracket.get_participant(match.player1_id)
            else:
                continue
            if match.player2_id is not None:
                participant2 = await bracket.get_participant(match.player2_id)
            else:
                prev_match = await bracket.get_match(match.player2_prereq_match_id)
                c = await challonge.get_user(os.getenv("CHALLONGE_USERNAME"), os.getenv("CHALLONGE_PASSWORD"))
                participant2 = challonge.Participant(c,{},bracket)
                participant2.name = f"Winner of Match {prev_match.identifier}"
                participant2.misc = "TBD"

        pairings.append((participant1,participant2))

    return pairings


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
    divisions = group_divisions(entries)
    single_entry_div = []
    for key, competitors in divisions.items():
        age_group = key.split("_")[1]
        gender = key.split("_")[2]
        weight_class = key.split("_")[3]
        print(f"Group {key}:")
        if len(competitors) == 1:
            single_entry_div.append(competitors[0])
            print(f"Single competitor {competitors[0]['name']} added to exhibition list.")
        else:
            loop = asyncio.get_event_loop()
            bracket = loop.run_until_complete(generate_division_bracket(key, competitors))
            print(f"Bracket: {bracket.live_image_url}")
            matches = [
                "#Game Gr.,#Class,#Gender,#Weight,#Chung Name,#Chung Belongs To,#Hong Name,#Hong Belongs To"
            ]
            pairings = loop.run_until_complete(get_match_details(bracket))
            for i, pairing in enumerate(pairings, start=1):
                participant1,participant2 = pairing
                print(
                    f'  Match {i}: {participant1.name} ({participant1.misc}) vs {participant2.name} ({participant2.misc})'
                )

                matches.append(
                    f"\n{i},{age_group},{gender},{weight_class},{participant1.name},{participant1.misc},{participant2.name},{participant2.misc}"
                )
            # upload_to_s3("".join(matches), f"{key}.csv")

    exhibition_entries = ["name,belt,age,gender,weight,weight_class,school"]
    for entry in single_entry_div:
        exhibition_entries.append(
            f"\n{entry['name']},{entry['belt']},{entry['age']},{entry['gender']},{entry['weight']},{entry['weight_class']},{entry['school']}"
        )
    # upload_to_s3("".join(exhibition_entries), "exhibition_entries.csv")


if __name__ == "__main__":
    main()