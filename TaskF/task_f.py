# Copyright (c) 2026 Lenn Fischer
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Created by Lenn Fischer according to given task

"""
Interactive program for analyzing electricity consumption and production data.
"""

import calendar
from datetime import datetime, timezone
import os

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
    converted.append(float(electricity_data[1].replace(",", ".")))  # netto_consumption (kWh)
    converted.append(float(electricity_data[2].replace(",", ".")))  # netto_production (kWh)
    converted.append(float(electricity_data[3].replace(",", ".")))  # Temperature (°C)
    return converted    

## Menu ##
def show_main_menu() -> str:
    """Prints the main menu and returns the user selection as a string."""
    print("Main Menu:")
    print("1. Create Daily Report for a Date Range")
    print("2. Create Monthly Report for one Month")
    print("3. Create Yearly Report for one Year")
    print("4. Exit")
    
    selection = input("Please select an option (1-4): ")
    return selection.strip()

def show_report_menu(report_lines: list[str]) -> None:
    """Prints the report output menu and returns the user selection as a string."""
    

    print("Report Output Menu:")
    print("1. Write report to 'report.txt'")
    print("2. Create a new report")
    print("3. Exit")
    
    while True:
        selection = input("Please select an option (1-3): ").strip()
        if selection == "1":
            write_report_to_file(report_lines)
            print("Report written to 'report.txt'.")
            break
        elif selection == "2":
            create_report_file(report_lines)
            print("Report written to new file.")
            break
        elif selection == "3":
            print ("Returning to Main Menu...")
            break
    
## Report Generation Functions ##
def create_daily_report(data: list) -> list[str]:
    """Builds a daily report for a selected date range."""
    print("Creating Daily Report...")
    tz = data[0][0].tzinfo if data else timezone.utc  # Use timezone from data or default to UTC

    start_date = None
    end_date = None
    while True:
        print("Please enter the start date (dd.mm.yyyy):")
        try: 
            start_date_str = input().strip()
            start_date = datetime.strptime(start_date_str, "%d.%m.%Y").replace(tzinfo=tz)
        except ValueError:
            print("Invalid date format. Please try again.")
            continue
        break
    while True: 
        print("Please enter the end date (dd.mm.yyyy):")
        try: 
            end_date_str = input().strip()
            end_date = datetime.strptime(end_date_str, "%d.%m.%Y").replace(hour=23, minute=59, second=59, microsecond=999999,tzinfo=tz)
        except ValueError:
            print("Invalid date format. Please try again.")
            continue
        break
    print(f"Creating Daily Report for the date range {start_date_str} to {end_date_str}...")

    report_lines = []
    report_lines.append(f"Daily Report for {start_date.strftime('%d.%m.%Y')} to {end_date.strftime('%d.%m.%Y')}")
    report_lines.append(f"Total Consumption: {format_float(calculate_total_consumption(data, start_date, end_date))} kWh")
    report_lines.append(f"Total Production: {format_float(calculate_total_production(data, start_date, end_date)) } kWh")
    report_lines.append(f"Average Temperature: {format_float(calculate_average_temperature(data, start_date, end_date))} °C")

    return report_lines 

def create_monthly_report(data: list) -> list[str]:
    """Builds a monthly summary report for a selected month."""
    print("Creating Monthly Report...")
    month = None
    tz = data[0][0].tzinfo if data else timezone.utc  # Use timezone from data or default to UTC

    print ("Please enter the month for the report (MM):")
    while True:
        month_str = input().strip()
        if month_str.isdigit() and 1 <= int(month_str) <= 12:
            month = int(month_str)
            break
        print("Invalid month. Please enter a number between 1 and 12.")

    report_lines = []
    report_lines.append(f"Monthly Report for {calendar.month_name[month]}")
    report_lines.append(f"Total Consumption: {format_float(calculate_total_consumption(data, datetime(2025, month, 1,0,0,0,0).replace(tzinfo=tz), datetime(2025, month, calendar.monthrange(2025,month)[1],23,59,59,999999).replace(tzinfo=tz)))} kWh")
    report_lines.append(f"Total Production: {format_float(calculate_total_production(data, datetime(2025, month, 1,0,0,0,0).replace(tzinfo=tz), datetime(2025, month, calendar.monthrange(2025,month)[1],23,59,59,999999).replace(tzinfo=tz)))} kWh")
    report_lines.append(f"Average Temperature: {format_float(calculate_average_temperature(data, datetime(2025, month, 1,0,0,0,0).replace(tzinfo=tz), datetime(2025, month, calendar.monthrange(2025,month)[1],23,59,59,999999).replace(tzinfo=tz)))} °C")
    return report_lines

def create_yearly_report(data: list) -> list[str]:
    """Builds a full-year summary report."""
    print("Creating Yearly Report...")
    tz=data[0][0].tzinfo if data else timezone.utc  # Use timezone from data or default to UTC
    report_lines = []

    report_lines.append("Yearly Report for 2025")
    report_lines.append(f"Total Consumption: {format_float(calculate_total_consumption(data, datetime(2025, 1, 1,0,0,0,0).replace(tzinfo=tz), datetime(2025, 12, 31,23,59,59,999999).replace(tzinfo=tz)))} kWh")
    report_lines.append(f"Total Production: {format_float(calculate_total_production(data, datetime(2025, 1, 1,0,0,0,0).replace(tzinfo=tz), datetime(2025, 12, 31,23,59,59,999999).replace(tzinfo=tz)))} kWh")
    report_lines.append(f"Average Temperature: {format_float(calculate_average_temperature(data, datetime(2025, 1, 1,0,0,0,0).replace(tzinfo=tz), datetime(2025, 12, 31,23,59,59,999999).replace(tzinfo=tz)))} °C")
    return report_lines

## Calculation Functions ## 
def calculate_total_consumption(data: list, start_date: datetime, end_date: datetime) -> float:
    """Calculates total electricity consumption for a given date range."""
    total_consumption = 0.0
    for entry in data:
        timestamp = entry[0]
        if start_date <= timestamp <= end_date:
            total_consumption += entry[1]  # netto_consumption
    return total_consumption

def calculate_total_production(data: list, start_date: datetime, end_date: datetime) -> float:
    """Calculates total electricity production for a given date range."""
    total_production = 0.0
    for entry in data:
        timestamp = entry[0]
        if start_date <= timestamp <= end_date:
            total_production += entry[2]  # netto_production
    return total_production

def calculate_average_temperature(data: list, start_date: datetime, end_date: datetime) -> float:
    """Calculates average temperature for a given date range."""
    total_temperature = 0.0
    count = 0
    for entry in data:
        timestamp = entry[0]
        if start_date <= timestamp <= end_date:
            total_temperature += entry[3]  # Temperature
            count += 1
    return total_temperature / count if count > 0 else 0.0



## Report Output Functions ##
def print_report_to_console(lines: list[str]) -> None:
    """Prints report lines to the console."""
    print("\nReport:")
    for line in lines:
        print(line)

    print("-" * 40 + "\n")  # Separator line
    
def create_report_file(lines: list[str]) -> None:
    """Creates a report file with the given lines."""
    counter = 1
    while True:
        filename = f"report_{counter}.txt"
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                for line in lines:
                    f.write(line + "\n")
            print(f"Report created: {filename}")
            break
        counter += 1

def write_report_to_file(lines: list[str]) -> None:
    """Writes report lines to the file report.txt."""
    print("Writing report to file 'report.txt'...")
    with open("report.txt", "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

def format_float(value: float) -> str:
    """Formats a float with two decimals and comma separator."""
    return f"{value:.2f}".replace(".", ",")

def main() -> None:
    """
Main function to run the electricity data analysis program.
Loads data, displays the main menu, and handles user interactions for generating reports.
    """ 
    electricity_data_file = "2025.csv"
    electricity_data = fetch_electricity_data(electricity_data_file)
    
    if not electricity_data:
        print("No data available to generate reports.")
        return
    
    while True:
        selection = show_main_menu()
        
        if selection == "1":
            report_lines = create_daily_report(electricity_data)
            print_report_to_console(report_lines)
            show_report_menu(report_lines)
        elif selection == "2":
            report_lines = create_monthly_report(electricity_data)
            print_report_to_console(report_lines)
            show_report_menu(report_lines)
        elif selection == "3":
            report_lines = create_yearly_report(electricity_data)
            print_report_to_console(report_lines)
            show_report_menu(report_lines)
        elif selection == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose a valid option (1-4).")
            continue
        
    
    


if __name__ == "__main__":
    main()