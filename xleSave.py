import pandas as pd
import os

def saveToXle(data,excel_filename):
    new_df = pd.DataFrame(data)
    if os.path.isfile(excel_filename):
            # Load the existing data from the Excel file
            existing_df = pd.read_excel(excel_filename)
            
            # Concatenate the existing data with the new data
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df
    
    # Save the combined DataFrame to the Excel file
    combined_df.to_excel(excel_filename, index=False)
    print(f'Data updated and saved to {excel_filename}')

def count_data_entries(excel_filename):
    df = pd.read_excel(excel_filename)
    num_entries = len(df) - 1
    # print(f"Number of data entries (excluding index): {num_entries}")
    return num_entries

