#!/bin/env python3

import csv
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="spieler-plus-csv-converter.py",
        description="Convert csv files downloaded from volleyball-nordbaden.de to import them to Spieler Plus.",
    )
    parser.add_argument("filename")
    parser.add_argument(
        "--home-team",
        required=True,
        help="Name of the home team as it appers in the input csv",
    )
    args = parser.parse_args()

    print(
        "Starting to convert csv file assuming that home team is called '"
        + args.home_team
        + "'."
    )

    # Define the input and output file paths
    input_file = args.filename
    output_file = "spielerplus.csv"

    output_data = []

    # Process the rows and convert the data format
    with open(input_file, "r", newline="", encoding="ISO-8859-1") as file:
        reader = csv.DictReader(file, delimiter=";")
        for input_row in reader:
            home_game = True if (input_row["Mannschaft 1"] == args.home_team) else False

            output_row = {}
            output_row["Spieltyp"] = "Spiel"
            output_row["Gegner"] = (
                input_row["Mannschaft 2"] if home_game else input_row["Mannschaft 1"]
            )
            output_row["Start-Datum"] = input_row["Datum"]
            output_row["End-Datum (Optional)"] = ""
            output_row["Start-Zeit"] = input_row["Uhrzeit"]
            output_row["Treffen (Optional)"] = ""
            output_row["End-Zeit (Optional)"] = ""
            output_row["Heimspiel"] = "ja" if home_game else "nein"
            output_row["Gelände / Räumlichkeiten"] = ""
            output_row["Adresse (optional)"] = input_row["Austragungsort"]
            output_row["Infos zum Spiel"] = "Spiel #" + input_row["#"]
            output_row["Teilname"] = "Spieler müssen zusagen"
            output_row["Nominierung"] = "Trainer,Spieler"
            output_row["Zu-/Absagen bis (Stunden vor dem Termin)"] = 48
            output_row["Erinnerung zum Zu-/Absagen (Stunden vor dem Termin)"] = 72

            output_data.append(output_row)

    # Write the list of dictionaries to the CSV file
    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=output_data[0].keys(), delimiter=";")

        writer.writeheader()
        writer.writerows(output_data)

    print(
        "The CSV file has been successfully converted and saved as '"
        + output_file
        + "'."
    )
