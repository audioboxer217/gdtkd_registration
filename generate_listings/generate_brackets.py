import os
import random
import generate_listings as gl

competition_name = os.getenv("COMPETITION_NAME").replace(" ","_")

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


def group_divisions(entries):
    divisions = {}
    sparring_entries = list(
        filter(lambda x: "sparring" in x["events"].split(","), entries)
    )
    for entry in sparring_entries:
        age_group = gl.get_age_group(entry)
        belt_group = get_belt_group(entry)
        key = f"{belt_group}_{age_group}_{entry['gender'][0]}_{entry['weight_class']}"
        if key not in divisions:
            divisions[key] = []
        divisions[key].append(entry)

    sparring_gr_entries = list(
        filter(lambda x: "sparring-gr" in x["events"].split(","), entries)
    )
    for entry in sparring_gr_entries:
        age_group = gl.get_age_group(entry)
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
        age_group = gl.get_age_group(entry)
        belt_group = get_belt_group(entry)
        key = (
            f"{belt_group}-wc_{age_group}_{entry['gender'][0]}_{entry['weight_class']}"
        )
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


def main():
    entries = gl.get_current_entries()
    entries = gl.set_weight_class(entries)
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
            bracket = generate_division_bracket(competitors)
            matches = [
                "#Game Gr.,#Class,#Gender,#Weight,#Chung Name,#Chung Belongs To,#Hong Name,#Hong Belongs To"
            ]
            for i, pairing in enumerate(bracket, start=1):
                participant1,participant2 = pairing
                print(
                    f'  Match {i}: {participant1["name"]} ({participant1["school"]}) vs {participant2["name"]} ({participant2["school"]})'
                )

                matches.append(
                    f"\n{i},{age_group},{gender},{weight_class},{participant1['name']},{participant1['school']},{participant2['name']},{participant2['school']}"
                )
            # gl.upload_to_s3("".join(matches), f"{key}.csv")

    exhibition_entries = ["name,belt,age,gender,weight,weight_class,school"]
    for entry in single_entry_div:
        exhibition_entries.append(
            f"\n{entry['name']},{entry['belt']},{entry['age']},{entry['gender']},{entry['weight']},{entry['weight_class']},{entry['school']}"
        )
    # gl.upload_to_s3("".join(exhibition_entries), "exhibition_entries.csv")


if __name__ == "__main__":
    main()