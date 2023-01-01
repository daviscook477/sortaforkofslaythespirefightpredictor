import json

from common import InvalidRunError, ModdedDataError, StSGlobals

in_file = "the_guardian_ironclad.json"

def out_file(i):
  return f"the_guardian_ironclad{i}.json"

def chunks(lst, n):
  """Yield successive n-sized chunks from lst."""
  for i in range(0, len(lst), n):
    yield lst[i:i + n]

def remove_invalid(card):
  """Removes cards from the deck that are considered invalid for training purposes"""
  for i in range(len(card)):
    # remove all curses and colorless cards from the decks
    card[i] = list(filter(lambda card: card not in StSGlobals.BASE_GAME_CURSES and card not in StSGlobals.BASE_GAME_COLORLESS_AND_UPGRADES, card[i]))

split_count = 32

def main():
  with open(in_file, 'r', encoding='utf-8') as f1:
    json_data = json.load(f1)
    cards = list(chunks(json_data, len(json_data) // split_count))
    for i in range(len(cards)):
      card = cards[i]
      remove_invalid(card)
      print(len(card))
      with open(out_file(i), 'w', encoding='utf-8') as f2:
        json.dump(card, f2, ensure_ascii=False)


if __name__ == "__main__":
  main()