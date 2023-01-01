# Fork of Alex's Fight Predictor Repo
I've modified this repo to use the run analysis tool Alex created for my own purposes.
Essentially just writing the data that it generates out in different formats.

## Encounter Data
I needed some sample decks for particular combat encounters so `main_encounter_stats.py` will take the processed runs and generate a json array of the cards in the player's deck when they entered a particular combat encounter. `split_encounter_stats.py` will take the encounter stats and split it into a bunch of separate files. It also removes some cards that are problematic for the self-play procedure and network such that they are ignored.