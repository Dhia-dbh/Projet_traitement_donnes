import pandas as pd
import time
from files_tools import read_lines_from_txt_file
from req import *
from print_arabic import *

# Function to write results to a CSV file using pandas


def write_results_to_csv(val, output_csv, n):
    quotes = set()  # Use a set to automatically handle duplicates

    # Classify each line individually
    for i in range(n):
        attempt = 0
        while attempt <= 4:  # Retry up to 4 times for errors
            try:
                quote = gemini_Generate(val)
                print_arabic(quote)
                # Check if the quote is already in the set
                if quote not in quotes:
                    quotes.add(quote)
                    break  # Exit the retry loop if successful
                else:
                    print(f"Duplicate quote detected, retrying...")
            except Exception as e:
                if "Resource has been exhausted" in str(e):
                    attempt += 1  # Increment attempt counter
                    # Exponential backoff (square the attempt number)
                    wait_time = 10
                    print(
                        f"Quota exceeded for line '{i}', retrying in {wait_time} seconds...")
                    time.sleep(wait_time)  # Wait before retrying
                else:
                    print(f"Failed to generate line '{i}': {e}")
                    break  # Exit the retry loop for non-quota-related errors

    # Convert the set of quotes to a list for DataFrame
    df = pd.DataFrame({
        'Line': list(quotes),
        'Category': val
    })

    # Write the DataFrame to a CSV file
    df.to_csv(output_csv, index=False)

# Main function


def main():
    """
    values = [  
    "التعاون",
    "التفاؤل",
    "التواصي بالخير",
    "التواضع",
    "الحذر واليقظة",
    "حسن السمت",
    "حسن الظن",
    "الحيطة",
    "الجود والكَرَم والسخاء والبذل",
    "الجدّية والحزم",
    "الحياء",
    "الحلم",
    "الحكمة",
    "حفظ اللسان",
    "حسن العشرة والجوار"]
    """
    values = ["البَشاشة"]

    # value = "الاحترام والتوقير"  # Category for quote generation
    for value in values:
        # Desired output CSV file name

        output_csv_path = f'/Generated data/{value}.csv'
        number_of_quotes = 300  # Number of quotes to generate
        write_results_to_csv(value, output_csv_path, number_of_quotes)
        print(f'Results written to {output_csv_path}')


if __name__ == '__main__':
    main()
