import sys
import constants
import requests
import json
import pandas as pd
import re
from datetime import datetime
import os
import logging

# Create and configure logger
logging.basicConfig(
    filename="Q.log", format="%(asctime)s %(levelname)s:%(message)s", filemode="w"
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_json(site_url):
    try:
        response = requests.get(site_url)
        return response.json()
    except requests.ConnectionError:
        logger.critical(f"Unable to get response from site {site_url}")
        quit()


def save_json(json_data, file_path):
    file = open(file_path, "w")
    json.dump(json_data, file, indent=4)
    file.close()


def read_json(file_path):
    return json.load(open(file_path))


def fetch_data(site_url, file_path):

    # If file is not found; a new json is being downloaded from the given url and saved as .json
    # File is being read as JSON
    if not os.path.exists(file_path):
        save_json(get_json(site_url), file_path)
    return read_json(file_path)


def remove_titles_and_honorifics(input_string):

    # Removes titles and honorifics from a sting based on list TITLES_AND_HONORIFICS found in constants
    return (" ").join(
        list(
            filter(
                lambda x: x.lower()
                not in list(map(lambda y: y.lower(), constants.TITLES_AND_HONORIFICS)),
                input_string.split(" "),
            )
        )
    )


def remove_roman_numerals(input_string):

    # Removes roman numbers from a string by using regex
    pattern = re.compile(
        r"^M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?$", re.VERBOSE
    )
    return (" ").join([s for s in input_string.split(" ") if not re.match(pattern, s)])


def create_name_cleaned(dataframe, name_column_cleaned):

    # Creates a new column with a cleaned name from where titles, honorifics and roman numbers are removed
    dataframe[name_column_cleaned] = (
        dataframe[constants.NAME_COLUMN]
        .apply(remove_roman_numerals)
        .apply(remove_titles_and_honorifics)
    )
    return dataframe


def create_firstname_lastname(dataframe, name_column):

    # Firstname and lastname columns are created by the name column
    # first name being the first item and last name being the last from the split name string
    dataframe[constants.FIRSTNAME_COLUMN] = dataframe[name_column].apply(
        lambda x: x.split(" ")[0]
    )
    dataframe[constants.LASTNAME_COLUMN] = dataframe[name_column].apply(
        lambda x: x.split(" ")[-1]
    )
    return dataframe


def create_report_dataframe(dataframe):
    df = pd.json_normalize(dataframe)
    name_column_cleaned = f"{constants.NAME_COLUMN}_cleaned"

    # Creates name_cleaned and firstname lastname columns
    df = create_name_cleaned(df, name_column_cleaned)
    df = create_firstname_lastname(df, name_column_cleaned)

    # Loops through REPORT_COLUMNS dictionary and adds renamed columns to empty dataframe
    output_df = pd.DataFrame()
    for column in constants.REPORT_COLUMNS:

        output_df[(constants.REPORT_COLUMNS[column])] = df[column]

    # Dataframe is being sorted
    output_df = output_df.sort_values(
        by=[
            constants.REPORT_COLUMNS[constants.LASTNAME_COLUMN],
            constants.REPORT_COLUMNS[constants.FIRSTNAME_COLUMN],
        ]
    )

    return output_df


def save_report_as_excel(input_dataframe, report_folder_path):

    # If missing, the folder is created
    if not os.path.exists(report_folder_path):
        os.makedirs(report_folder_path)

    creation_timestamp = datetime.now().strftime(constants.TIMESTAMP_FORMAT)
    report_sheet_name = f"{constants.REPORT_PREFIX}{creation_timestamp}"
    filepath = (
        f"{report_folder_path}/{constants.REPORT_PREFIX}{creation_timestamp}.xlsx"
    )

    # Creates the report and auto-adjusts column widths
    with pd.ExcelWriter(filepath) as writer:
        input_dataframe.to_excel(
            writer, sheet_name=report_sheet_name, index=False, na_rep="NaN"
        )
        for column in input_dataframe:
            column_length = max(
                input_dataframe[column].astype(str).map(len).max(), len(column)
            )
            col_idx = input_dataframe.columns.get_loc(column)
            writer.sheets[report_sheet_name].set_column(col_idx, col_idx, column_length)

    logger.info(f"Report was successfully saved to '{filepath}'")


def main():

    if len(sys.argv) > 2:
        logger.error("Only one argument is allowed!")
        quit()
    elif len(sys.argv) > 1:
        report_folder = sys.argv[1]
        logger.info(f"Report will be saved to path '{report_folder}'")
    else:
        report_folder = constants.DEFAULT_REPORTS_FOLDER
        logger.info(
            f"Report will be saved to default path '{constants.DEFAULT_REPORTS_FOLDER}'"
        )

    json_data = fetch_data(constants.URL, constants.FILE)
    report_dataframe = create_report_dataframe(json_data)
    save_report_as_excel(report_dataframe, report_folder)


if __name__ == "__main__":
    main()
