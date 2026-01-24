# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by Lenn Fischer according to given task

"""
A program that reads reservation data from a file
and prints them to the console using functions:

Reservation number: 123
Booker: Anna Virtanen
Date: 31.10.2025
Start time: 10.00
Number of hours: 2
Hourly rate: 19,95 €
Total price: 39,90 €
Paid: Yes
Venue: Meeting Room A
Phone: 0401234567
Email: anna.virtanen@example.com

"""
from datetime import datetime

def print_booker(reservation: list) -> None:
    """
    Prints the reservation number

    Parameters:
    reservation (lst): reservation -> columns separated by |
    """
    booker = str(reservation[1])
    print(f"Booker: {booker}")

def print_reservation_number(reservation: list) -> None:
    """
    Prints the reservation number

    Parameters:
    reservation (lst): reservation -> columns separated by |
    """
    reservation_number = int(reservation[0])
    print(f"Reservation number: {reservation_number}")

def print_date(reservation: list) -> None:  
    """
    Prints the reservation date

    Parameters:
    reservation (lst): reservation -> columns separated by |
    """
    reservation_date = datetime.strptime(reservation[2], "%Y-%m-%d").date()
    reservation_date_finnish_format = reservation_date.strftime("%d.%m.%Y")
    print(f"Date: {reservation_date_finnish_format}")

def print_start_time(reservation: list) -> None:
    """
    Prints the reservation start time

    Parameters:
    reservation (lst): reservation -> columns separated by |   
    """
    reservation_start_time = datetime.strptime(reservation[3], "%H:%M").time()
    reservation_time_finnish_format = reservation_start_time.strftime("%H.%M")
    print("Start time:", reservation_time_finnish_format)

def print_hours(reservation: list) -> None:
    """
    Prints the number of reserved hours
    
    Parameters:
    reservation (lst): reservation -> columns separated by |   
    """
    reservation_number_of_hours = int(reservation[4])
    print("Number of hours:", reservation_number_of_hours)

def print_hourly_price(reservation: list) -> None:
    """
    Prints the hourly price
    
    Parameters:
        reservation (lst): reservation -> columns separated by |
    """
    reservation_hourly_price = float(reservation[5])
    reservation_hourly_price_finnish_format = str("{0:.2f}".format(reservation_hourly_price).replace('.', ','))
    print("Hourly price:", reservation_hourly_price_finnish_format, "€")

def print_total_price(reservation: list) -> None:
    """
    Prints the total price

    Parameters:
        reservation (lst): reservation -> columns separated by |
    """
    reservation_total_price = int(reservation[4]) * float(reservation[5])
    reservation_total_price_finnish_format = str("{0:.2f}".format(reservation_total_price).replace('.', ','))
    print("Total price:", reservation_total_price_finnish_format, "€")

def print_paid(reservation: list) -> None:
    """
    Prints whether the reservation is paid
    Parameters:
        reservation (lst): reservation -> columns separated by |
    """
    reservation_paid = bool(reservation[6] == "True")
    print(f"Paid: {'Yes' if reservation_paid else 'No'}")

def print_location(reservation: list) -> None:
    """
    Prints the reservations location

    Parameters:
        reservation (lst): reservation -> columns separated by |
    """
    reservation_resource = str(reservation[7])
    print("Location:", reservation_resource)

def print_phone(reservation: list) -> None:
    """
    Prints the bookers phone number

    Parameters:
        reservation (lst): reservation -> columns separated by |
    """
    reservation_phone = str(reservation[8])
    print("Phone:", reservation_phone)

def print_email(reservation: list) -> None:
        """
        Prints the bookers email address

        Parameters:
            reservation (lst): reservation -> columns separated by |
        """
        reservation_email = str(reservation[9])
        print("Email:", reservation_email)

def main():
    """
    Reads reservation data from a file and
    prints them to the console using functions
    """
    # Define the file name directly in the code
    reservations = "reservations.txt"

    # Open the file, read it, and split the contents
    with open(reservations, "r", encoding="utf-8") as f:
        reservation = f.read().strip()
        reservation = reservation.split('|')

    # Implement the remaining parts following
    # the function print_booker(reservation)
    
    # The functions to be created should perform type conversions
    # and print according to the sample output

    print_reservation_number(reservation)
    print_booker(reservation)
    print_date(reservation)
    print_start_time(reservation)
    print_hours(reservation)
    print_hourly_price(reservation)
    print_total_price(reservation)
    print_paid(reservation)
    print_location(reservation)
    print_phone(reservation)
    print_email(reservation)

if __name__ == "__main__":
    main()