#!/bin/env python3

import csv
import argparse
from typing import List, Dict


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="spieler-plus-csv-converter.py",
        description="Convert csv files downloaded from volleyball-nordbaden.de to import them to Spieler Plus.",
    )
    parser.add_argument("filename")
    parser.add_argument(
        "--home-team",
        required=True,
        help="Name of the home team as it appears in the input csv",
    )
    return parser.parse_args()


def read_csv(input_file: str) -> List[Dict[str, str]]:
    with open(input_file, "r", newline="", encoding="ISO-8859-1") as file:
        reader = csv.DictReader(file, delimiter=";")
        return list(reader)


def create_output_row(
    game: Dict[str, str], home_team: str, game_number: int
) -> Dict[str, str]:
    home_game = True if (game["Mannschaft 1"] == home_team) else False

    output_row = {}
    output_row["Spieltyp"] = f"Spiel{game_number}"
    output_row["Gegner"] = game["Mannschaft 2"] if home_game else game["Mannschaft 1"]
    output_row["Start-Datum"] = game["Datum"]
    output_row["End-Datum (Optional)"] = ""
    output_row["Start-Zeit"] = game["Uhrzeit"]
    output_row["Treffen (Optional)"] = ""
    output_row["End-Zeit (Optional)"] = ""
    output_row["Heimspiel"] = "ja" if home_game else "nein"
    output_row["Gelände / Räumlichkeiten"] = ""
    output_row["Adresse (optional)"] = game["Austragungsort"]
    output_row["Infos zum Spiel"] = "Spiel #" + game["#"]
    output_row["Teilname"] = "Spieler müssen absagen"
    output_row["Nominierung"] = "Trainer,Spieler"
    output_row["Zu-/Absagen bis (Stunden vor dem Termin)"] = 48
    output_row["Erinnerung zum Zu-/Absagen (Stunden vor dem Termin)"] = 72

    return output_row


def process_data(rows: List[Dict[str, str]], home_team: str) -> List[Dict[str, str]]:
    output_data = []

    for i in range(0, len(rows), 2):
        game1 = rows[i]
        game2 = rows[i + 1]

        for index, game in enumerate([game1, game2]):
            # We don't play this one, no need to import it
            if game["Mannschaft 1"] != home_team and game["Mannschaft 2"] != home_team:
                continue

            game_number = index + 1
            output_row = create_output_row(game, home_team, game_number)
            output_data.append(output_row)

    return output_data


def write_csv(output_file: str, output_data: List[Dict[str, str]]):
    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=output_data[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(output_data)


def main():
    args = parse_arguments()
    print(
        "Starting to convert csv file assuming that home team is called '"
        + args.home_team
        + "'."
    )

    input_file = args.filename
    output_file = "spielerplus.csv"

    rows = read_csv(input_file)
    output_data = process_data(rows, args.home_team)
    write_csv(output_file, output_data)

    print(
        "The CSV file has been successfully converted and saved as '"
        + output_file
        + "'."
    )


if __name__ == "__main__":
    main()
