# Copyright (c) 2026 Lenn Fischer
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Created by Lenn Fischer according to given task

"""
Program for analyzing electricity consumption and production data from multiple CSV files.
"""

from datetime import datetime

## LOADING DATA ##
def fetch_electricity_data(electricity_data_file: str) -> list[list]:
    """
    Reads electricity data from a csv file and returns the data converted


    Parameters:
    electricity_data_file (str): Name of the file containing the electricity data

    Returns:
    electricity_data (list): Read and converted electricity data
    """
    electricity_data = []
    
    try:
        with open(electricity_data_file, "r", encoding="utf-8") as f:
            for line in f:
                fields = line.split(";")
                try:
                    # Skip header line
                    datetime.fromisoformat(fields[0])
                except ValueError:
                    continue
                electricity_data.append(convert_electricity_data(fields))
        return electricity_data
    except FileNotFoundError:
        print(f"Error: File '{electricity_data_file}' not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied when trying to read '{electricity_data_file}'.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def convert_electricity_data(electricity_data: list) -> list:
    """
    Convert data types to meet program requirements

    Parameters:
    electricity_data (list): Unconverted electricity data -> ?? columns

    Returns:
    converted (list): Converted data types
    """
    converted = []
    converted.append(datetime.fromisoformat(electricity_data[0]))  # timestamp
    converted.append(int(electricity_data[1]))  # consumption_phase_1 (Wh)
    converted.append(int(electricity_data[2]))  # consumption_phase_2 (Wh)
    converted.append(int(electricity_data[3]))  # consumption_phase_3 (Wh)
    converted.append(int(electricity_data[4]))  # production_phase_1 (Wh)
    converted.append(int(electricity_data[5]))  # production_phase_2 (Wh)
    converted.append(int(electricity_data[6]))  # production_phase_3 (Wh)
    return converted

def analyze_multiple_files(electricity_data_files: list[str]) -> list[tuple[str, list[list]]]:
    """
    Analyzes multiple electricity data files and returns their daily overviews.
    Parameters:
    electricity_data_files (list): List of file names containing the electricity data
    Returns:
    list_of_weekly_data (list): List of tuples containing file name and calculated daily overview
    """
    list_of_weekly_data =[]
    for file_name in electricity_data_files:
        electricity_data = fetch_electricity_data(file_name)

        calculated_daily_overview = calculate_daily_overview(electricity_data)
        list_of_weekly_data.append((file_name, calculated_daily_overview))
    
    return list_of_weekly_data

## Extracting and Formatting Data ##
def extract_week_name(file_name: str) -> str:
    """
    Extracts the week information from the file name.

    Parameters:
    file_name (str): The name of the file.

    Returns:
    str: The extracted week information.
    """
    base_name = file_name.split(".")[0]  # Remove file extension
    return base_name.replace("week", "Week ")  # Format week string

def get_day_name(date: datetime) -> str:
    """
    Returns the name of the day for a given date.

    Parameters:
    date (datetime): The date to get the day name for.

    Returns:
    str: The name of the day.
    """
    # day_name = date.strftime("%A")
    day_name = get_finnish_day_name(date.strftime("%A"))
    return day_name

def get_finnish_day_name(day_name: str) -> str:
    """
    Returns the Finnish name of the day for a given English day name.

    Parameters:
    day_name (str): The English name of the day.

    Returns:
    str: The Finnish name of the day.
    """
    days = {
        "Monday": "Maanantai",
        "Tuesday": "Tiistai",
        "Wednesday": "Keskiviikko",
        "Thursday": "Torstai",
        "Friday": "Perjantai",
        "Saturday": "Lauantai",
        "Sunday": "Sunnuntai",
    }
    return days.get(day_name, day_name)

def format_data(data: float) -> str:
    """
    Formats the data to two decimal places, adding a leading space if less than 10.0 and replaces dot with comma.

    Parameters:
    data (float): The data to format.

    Returns:
    str: The formatted data.
    """
    formated_data = (
        f" {data:.2f}".replace(".", ",")
        if data < 10.0
        else f"{data:.2f}".replace(".", ",")
    )
    return formated_data

## Calculations ##
def calculate_daily_overview(electricity_data: list[list]) -> list[list]:
    """
    Calculates the daily overview of electricity consumption
    and production in kWh ordered by phase.

    Parameters:
    electricity_data (list): List of electricity data records
    """

    daily_sums = {}

    for record in electricity_data:       
        d = record[0].date()           # date

        if d not in daily_sums:
            daily_sums[d] = [record[0], 0, 0, 0, 0, 0, 0]

        daily_sums[d][1] += record[1]  # consumption phase 1 (Wh)
        daily_sums[d][2] += record[2]  # consumption phase 2 (Wh)
        daily_sums[d][3] += record[3]  # consumption phase 3 (Wh)
        daily_sums[d][4] += record[4]  # production  phase 1 (Wh)
        daily_sums[d][5] += record[5]  # production  phase 2 (Wh)
        daily_sums[d][6] += record[6]  # production  phase 3 (Wh)

    calculated_daily_data = []
    for d in sorted(daily_sums.keys()):
        ts, c1, c2, c3, p1, p2, p3 = daily_sums[d]
        calculated_daily_data.append([
            ts,
            c1 / 1000, # consumption phase 1 (kWh)
            c2 / 1000, # consumption phase 2 (kWh)
            c3 / 1000, # consumption phase 3 (kWh)
            p1 / 1000, # production  phase 1 (kWh)
            p2 / 1000, # production  phase 2 (kWh)
            p3 / 1000, # production  phase 3 (kWh)
        ])

    return calculated_daily_data

def calculate_weekly_summary(calculated_daily_overview: list[list]) -> list:
    """
    Calculates the weekly summary of electricity consumption
    and production in kWh ordered by phase.
    Parameters:
    calculated_daily_overview (list): The calculated daily overview data
    weekly_summary (list): Weekly summary of consumption and production [c1, c2, c3, p1, p2, p3]
    Returns:
    list: The weekly summary data
    """
    weekly_summary = [0, 0, 0, 0, 0, 0]  # [c1, c2, c3, p1, p2, p3]
    for day in calculated_daily_overview:
        weekly_summary[0] += day[1]  # c1
        weekly_summary[1] += day[2]  # c2
        weekly_summary[2] += day[3]  # c3
        weekly_summary[3] += day[4]  # p1
        weekly_summary[4] += day[5]  # p2
        weekly_summary[5] += day[6]  # p3

    return weekly_summary

def calculate_total_summary(weekly_summaries: list[list]) -> list:
    """
    Calculates the total summary of electricity consumption
    and production in kWh ordered by phase across multiple weeks.
    Parameters:
    weekly_summaries (list): List of weekly summaries
    Returns:
    list: The total summary data
    """
    total_summary = [0, 0, 0, 0, 0, 0]  # [c1, c2, c3, p1, p2, p3]
    for weekly_summary in weekly_summaries:
        total_summary[0] += weekly_summary[0]  # c1
        total_summary[1] += weekly_summary[1]  # c2
        total_summary[2] += weekly_summary[2]  # c3
        total_summary[3] += weekly_summary[3]  # p1
        total_summary[4] += weekly_summary[4]  # p2
        total_summary[5] += weekly_summary[5]  # p3
    return total_summary

## Report Generation ##
def generate_report(output_file_name: str, file_names: list[str]) -> None:
    """
    Generates and prints text file with a report of the electricity consumption
    and production in kWh ordered by phase for multiple weeks.
    Parameters:
    output_file_name (str): The name of the output report file
    file_names (list): List of file names containing the electricity data
    """
    analyzed_weekly_data = analyze_multiple_files(file_names)
    weekly_summaries = []

    report_string = ""

    for week_data in analyzed_weekly_data:
        file_name, calculated_daily_overview = week_data
        calculated_weekly_summary = calculate_weekly_summary(calculated_daily_overview)
        weekly_summaries.append(calculated_weekly_summary)

        report_string += generate_daily_overview_string(file_name, calculated_daily_overview)
        report_string += generate_weekly_summary_string(file_name, calculated_weekly_summary)

    report_string += generate_total_summary_string(calculate_total_summary(weekly_summaries))

    print(report_string)
    try:
        with open(output_file_name + ".txt", "w", encoding="utf-8") as f:
            f.write(report_string)
    except Exception as e:
        print(f"An error occurred while writing the report file: {e}")

## Report Formatting ##
def generate_daily_overview_string(file_name: str, calculated_daily_overview: list) -> str:
    """
    Generates a string representation of the daily overview for the provided electricity data file.
    Parameters:
    file_name (str): The name of the file containing the electricity data
    calculated_daily_overview (list): The calculated daily overview data
    Returns:
    str: The formatted daily overview string
    """
    overview_string = ""
    overview_string += "-------------------------------------------------------------------------------\n"
    overview_string += "\n"
    overview_string += (
        f"{extract_week_name(file_name)} electricity consumption and production (kWh, by phase)\n"
    )
    overview_string += "\n"
    overview_string += "Päivä         Päivämäärä     Kulutus [kWh]                  Tuotanto [kWh]\n"
    overview_string += "              (dd.mm.yyyy)   v1      v2      v3             v1     v2     v3\n"
    overview_string += "-------------------------------------------------------------------------------\n"
    for day_data in calculated_daily_overview:
        overview_string += (
            f"{get_day_name(day_data[0]):<15}{day_data[0].strftime('%d.%m.%Y')}    "
            f"{format_data(day_data[1])}   {format_data(day_data[2])}   {format_data(day_data[3])}          "
            f"{format_data(day_data[4])}  {format_data(day_data[5])}  {format_data(day_data[6])}\n"
        )
    overview_string += "-------------------------------------------------------------------------------\n"
    return overview_string

def generate_weekly_summary_string(file_name: str, weekly_summary: list) -> str:
    """
    Generates a string representation of the weekly summary for the provided electricity data file.
    Parameters:
    file_name (str): The name of the file containing the electricity data
    weekly_summary (list): Weekly summary of consumption and production [c1, c2,
    c3, p1, p2, p3]
    Returns:
    str: The formatted weekly summary string
    """
    summary_string = ""
    summary_string += (
        f"Summary for {extract_week_name(file_name)}:        "
        f"{format_data(weekly_summary[0]):<9}"
        f"{format_data(weekly_summary[1]):<8}"
        f"{format_data(weekly_summary[2]):<15}"
        f"{format_data(weekly_summary[3]):<7}"
        f"{format_data(weekly_summary[4]):<7}"
        f"{format_data(weekly_summary[5]):<8}\n"
    )
    return summary_string

def generate_total_summary_string(total_summary: list) -> str:
    """
    Generates a string representation of the total summary for all provided electricity data files.
    Parameters:
    total_summary (list): Total summary of consumption and production [c1, c2,
    c3, p1, p2, p3]
    Returns:
    str: The formatted total summary string
    """
    total_summary_string = ""
    total_summary_string += "\n"
    total_summary_string += "###############################################################################\n"
    total_summary_string += (
        f"Total Summary:              "
        f"{format_data(total_summary[0]):<8}"
        f"{format_data(total_summary[1]):<9}"
        f"{format_data(total_summary[2]):<15}"
        f"{format_data(total_summary[3]):<7}"
        f"{format_data(total_summary[4]):<7}"
        f"{format_data(total_summary[5]):<8}\n"
    )
    total_summary_string += "###############################################################################\n"
    return total_summary_string




def main() -> None:
    """
    Generates and prints a report of the electricity consumption
    and production in kWh ordered by phase for multiple weeks.
    """
    file_names = ["week41.csv", "week42.csv", "week43.csv"]
    output_file_name = "summary"

    generate_report(output_file_name,file_names)


if __name__ == "__main__":
    main()
