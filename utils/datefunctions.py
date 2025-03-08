# Imports
import datetime

# This module provides date-related functions and constants.
if __name__ == "__main__":
    print("This module is not meant to be run directly.")

TODAY = datetime.date.today()
VAYCAY_START = datetime.date(2025, 6, 19)
DAYS_UNTIL_VAYCAY = (VAYCAY_START - TODAY).days

def get_days_until_vaycay():
    return f"{DAYS_UNTIL_VAYCAY} until vaycay!"