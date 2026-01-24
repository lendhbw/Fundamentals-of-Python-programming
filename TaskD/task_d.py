# Copyright (c) 2026 Lenn Fischer
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Created by Lenn Fischer according to given task

"""
A program that provides a daily overview of the electricity consumption
and production in kWh ordered by phase, by reading a CSV file with hourly
measurments in the format of 'week42.csv'.
"""

from datetime import datetime


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


def test_print(electricity_data: list) -> None:
    """
    Test print function to verify data reading and conversion

    Parameters:
    electricity_data (list): Electricity data to print
    """
    for record in electricity_data:
        for value in record:
            print(f"  {value} ({type(value)})", end="")
        print()


def output_print(file_name: str, calculated_daily_overview: list) -> None:
    """
    Prints the final and formatted Overview as a table

    Parameters:
    file_name (str): The name of the file containing the electricity data

    """
    print()
    print(
        f"{extract_week(file_name)} electricity consumption and production (kWh, by phase)"
    )
    print()
    # print("Day         Date           Consumption [kWh]              Production [kWh]")
    print("Päivä         Päivämäärä     Kulutus [kWh]                  Tuotanto [kWh]")
    print("              (dd.mm.yyyy)   v1      v2      v3             v1     v2     v3")
    print("-------------------------------------------------------------------------------")
    for day_data in calculated_daily_overview:
        print(
            f"{get_day_name(day_data[0]):<15}{day_data[0].strftime('%d.%m.%Y')}    "
            f"{format_data(day_data[1])}   {format_data(day_data[2])}   {format_data(day_data[3])}          "
            f"{format_data(day_data[4])}  {format_data(day_data[5])}  {format_data(day_data[6])}"
        )


def extract_week(file_name: str) -> str:
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


def calculate_daily_overview(electricity_data: list[list]) -> list[list]:
    """
    Calculates and prints the daily overview of electricity consumption
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


def main() -> None:
    """
    Prints a daily overview of the electricity consumption
    and production in kWh ordered by phase
    """
    file_name = "week42.csv"

    electricity_data = fetch_electricity_data(file_name)

    calculated_daily_overview = calculate_daily_overview(electricity_data)

    output_print(file_name, calculated_daily_overview)
    # test_print(calculated_daily_overview)


if __name__ == "__main__":
    main()
