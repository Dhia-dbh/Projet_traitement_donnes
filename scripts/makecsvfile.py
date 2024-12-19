import pandas as pd

def convert_text_to_csv(input_txt_path, output_csv_path, category_label):
    # Read the text file into a list, stripping whitespace and skipping empty lines
    with open(input_txt_path, 'r') as txt_file:
        content_lines = [line.strip() for line in txt_file if line.strip()]
    
    # Create a DataFrame with 'Line' and 'Category' columns
    data_frame = pd.DataFrame({
        "Line": content_lines,
        "Category": category_label  # this will apply the same category to all rows
    })
    
    # Remove duplicate rows based on the 'Line' column
    data_frame = data_frame.drop_duplicates(subset="Line")
    
    # Write the DataFrame to a CSV file
    data_frame.to_csv(output_csv_path, index=False)

# Set the category value and output path
category_value = "الفطنة والذكاء"
output_csv_path = f'./Generated data/{category_value}.csv'
input_txt_path = f'./Raw data/{category_value}.txt'
# Example usage
convert_text_to_csv(input_txt_path, output_csv_path, category_value)
