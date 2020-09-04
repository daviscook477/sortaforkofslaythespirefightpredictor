import json

out_file = "hexaghost_ironclad.json"
in_files = ["out\\2020-09-03\\data_2020-09-03_0.json",
"out\\2020-09-03\\data_2020-09-03_1.json",
"out\\2020-09-03\\data_2020-09-03_2.json",
"out\\2020-09-03\\data_2020-09-03_3.json"]

def main():
    cards = []
    for in_file in in_files:
        with open(in_file, 'r', encoding='utf-8') as f1:
            json_data = json.load(f1)
            for run in json_data:
                for encounter in run:
                    # skip any run thats not the ironclad
                    if encounter['character'] != 'IRONCLAD':
                        break
                    # skip any run thats not ascension 20
                    # this should filter out bad players
                    # that are making terrible deck decisions
                    # from impacting the results too much
                    if encounter['ascension'] < 20:
                        break
                    # only look at the specific encounter once per run
                    if encounter['encounter'] == 'Hexaghost':
                        cards.append(encounter['cards'])
                        break

    print(len(cards))
    with open(out_file, 'w', encoding='utf-8') as f2:
        json.dump(cards, f2, ensure_ascii=False)

if __name__ == "__main__":
    main()
