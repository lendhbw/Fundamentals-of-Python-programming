# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

"""
Program that reads reservation details from a file
and prints them to the console:

Reservation number: 123
Booker: Anna Virtanen
Date: 31.10.2025
Start time: 10.00
Number of hours: 2
Hourly price: 19,95 €
Total price: 39,90 €
Paid: Yes
Location: Meeting Room A
Phone: 0401234567
Email: anna.virtanen@example.com
"""

from datetime import datetime


def main():
    # Define the file name directly in the code
    reservations = "reservations.txt"

    # Open the file and read its contents
    with open(reservations, "r", encoding="utf-8") as f:
        reservation = f.read().strip()

    reservation_details = reservation.split('|')
    reservation_number = int(reservation_details[0])
    reservation_booker = str(reservation_details[1])
    reservation_date = datetime.strptime(reservation_details[2], "%Y-%m-%d").date()
    reservation_date_finnish_format = reservation_date.strftime("%d.%m.%Y")
    reservation_start_time = datetime.strptime(reservation_details[3], "%H:%M").time()
    reservation_time_finnish_format = reservation_start_time.strftime("%H.%M")
    reservation_number_of_hours = int(reservation_details[4])
    reservation_hourly_price = float(reservation_details[5])
    reservation_hourly_price_finnish_format = str("{0:.2f}".format(reservation_hourly_price).replace('.', ','))
    reservation_total_price = reservation_hourly_price * reservation_number_of_hours 
    reservation_total_price_finnish_format = str("{0:.2f}".format(reservation_total_price).replace('.', ','))
    reservation_paid = bool(reservation_details[6] == "True")
    reservation_resource = str(reservation_details[7])
    reservation_phone = str(reservation_details[8])
    reservation_email = str(reservation_details[9])

    print("Reservation number:", reservation_number)
    print("Booker:", reservation_booker)
    print("Date:", reservation_date_finnish_format)
    print("Start time:", reservation_time_finnish_format)
    print("Number of hours:", reservation_number_of_hours)
    print("Hourly price:", reservation_hourly_price_finnish_format, "€")
    print("Total price:", reservation_total_price_finnish_format, "€")
    print(f"Paid: {'Yes' if reservation_paid else 'No'}")
    print("Location:", reservation_resource)
    print("Phone:", reservation_phone)
    print("Email:", reservation_email)
    


    # Print the reservation to the console
    # print(reservation)

    # Try these
    #print(reservation.split('|'))
    #reservationId = reservation.split('|')[0]
    #print(reservationId)
    #print(type(reservationId))
    """
    The above should have printed the number 123,
    which is by default text.

    You can also try changing [0] to [1]
    and test what changes.
    """

if __name__ == "__main__":
    main()