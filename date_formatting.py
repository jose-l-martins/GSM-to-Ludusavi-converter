# date_formatting.py
import os
import random


# Extract date from GSM filename in a DateTime Stamp format and convert it to ISO 8601 format
def convert_filename_to_iso_timestamp(gsm_file: str):
    file_name_without_extension = os.path.splitext(gsm_file)[0]

    # Extract the last 19 characters from the file name
    date_string = file_name_without_extension[-19:]

    # Convert the date string to ISO 8601 format
    date_string = date_string.replace("_", "T").replace("-", "").replace(".", "") + "Z"
    return date_string


# Extract date from GSM filename in a DateTime Stamp ("YYYY-MM-DD_HH.MM.SS") format and convert it to ISO-Timestamp hybrid format ("YYYY-MM-DD-THH:MM:SSZ")
def convert_filename_to_hybrid_timestamp(gsm_file: str, with_fractional_seconds: bool = False):
    file_name_without_extension = os.path.splitext(gsm_file)[0]
    
    # Extract the last 19 characters from the file name
    date_string = file_name_without_extension[-19:]
    
    # Convert the date string to ISO hybrid format
    date_string = date_string.replace("_", "T").replace(".", ":")
    
    if with_fractional_seconds:
        # Create string with 9 random integers
        nine_random_integers = [random.randint(0, 9) for _ in range(9)]
        nine_integers_string = ''.join(str(num) for num in nine_random_integers)
        date_string = date_string + "." + nine_integers_string
    
    # Indicates the UTC time zone
    date_string = date_string + "Z"
    return date_string