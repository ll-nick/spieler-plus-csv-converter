# Spieler Plus CSV Converter

Convert csv files downloaded from volleyball-nordbaden.de to a format used by Spieler Plus to easily import games.

Usage example: `python convert-csv.py --home-team "Your Team Name" input.csv`

The converted csv will be written to `spielerplus.csv`. Use the office program of your choice to convert the csv file to an xlsx file (`;` are used as delimiters) and upload it to Spieler Plus.

If you want to the address of game locations, you may need to adjust the data in the table to match the data in the Spieler Plus location management.