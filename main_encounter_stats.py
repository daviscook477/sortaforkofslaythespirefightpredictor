import json

out_file = "the_guardian_ironclad.json"
in_files = ["C:\\Users\davis\Documents\Slay the Spire Runs\\2023-01-01\\data_2023-01-01_0.json",
"C:\\Users\davis\Documents\Slay the Spire Runs\\2023-01-01\\data_2023-01-01_1.json",
"C:\\Users\davis\Documents\Slay the Spire Runs\\2023-01-01\\data_2023-01-01_2.json",
"C:\\Users\davis\Documents\Slay the Spire Runs\\2023-01-01\\data_2023-01-01_3.json",
"C:\\Users\davis\Documents\Slay the Spire Runs\\2023-01-01\\data_2023-01-01_4.json",
"C:\\Users\davis\Documents\Slay the Spire Runs\\2023-01-01\\data_2023-01-01_5.json",
"C:\\Users\davis\Documents\Slay the Spire Runs\\2023-01-01\\data_2023-01-01_6.json"]

def main():
    cards = []
    for in_file in in_files:
        with open(in_file, 'r', encoding='utf-8') as f1:
            json_data = json.load(f1)
            for run in json_data:
                for encounter in run:
                    # skip any run that lost at this fight
                    if encounter['entering_hp'] - encounter['damage_taken'] <= 0:
                        break
                    # skip any run thats not the ironclad
                    if encounter['character'] != 'IRONCLAD':
                        break
                    # skip any run thats not ascension 20
                    # this should filter out bad players
                    # that are making terrible deck decisions
                    # from impacting the results too much
                    if encounter['ascension'] < 15:
                        break
                    # only look at the specific encounter once per run
                    if encounter['encounter'] == 'The Guardian':
                        cards.append(encounter['cards'])
                        break

    print(len(cards))
    with open(out_file, 'w', encoding='utf-8') as f2:
        json.dump(cards, f2, ensure_ascii=False)

if __name__ == "__main__":
    main()
