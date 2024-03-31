import pandas as pd
import os

class FormationSector():
    def __init__(self, old_sheets, new_sheet, column_mapping):
        self.old_sheet_names = old_sheets
        self.new_sheet_name = new_sheet
        self.columns_mapping = column_mapping

    def createSheet(self):
        new_sheet_df = pd.DataFrame(columns=self.columns_mapping.keys())
        new_sheet_df.to_excel(self.new_sheet_name, index=False)
        print(f"New sheet '{self.new_sheet_name}' created successfully.")
        return new_sheet_df

    def dataTransformation(self):
        final_data = pd.DataFrame(columns=self.columns_mapping.keys())
        for old_sheet_name in self.old_sheet_names:
            try:
                old_sheet_df = pd.read_excel(old_sheet_name)
                selected_cols = [self.columns_mapping[col] for col in old_sheet_df.columns if col in self.columns_mapping]
                selected_data = old_sheet_df[selected_cols]
                if not selected_data.empty:  # Check if DataFrame is empty
                    selected_data.fillna('', inplace=True)
                    final_data = pd.concat([final_data, selected_data])
            except FileNotFoundError:
                print(f"File '{old_sheet_name}' not found.")
                continue
            except KeyError:
                print("Column mapping error. Please check your column mappings.")
                return None
        return final_data
    
    def delNaN(self, column):
        try:
            self.final_data = self.final_data.dropna(subset=[column])
            print(f"NaN values deleted from column '{column}'.")
        except KeyError:
            print(f"Column '{column}' not found in the DataFrame.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")



if __name__ == "__main__":
    old_sheets = ["dcd.xlsx"]  # Add more old sheet names if needed
    new_sheet = "wList.xlsx"
    column_mapping = {
        "Title": "Title",
        "Episode": "Episode",
        "Time": "Time",
        "Type": "Type",
        "Status": "Status",
        "Comment": "Comment",
    }
    print(f'Starting data processing...')
    fm = FormationSector(old_sheets, new_sheet, column_mapping)
    print(f'Data loaded...')
    if not os.path.exists(new_sheet):
        print(f'Creating new sheet...{new_sheet}.')
        fm.createSheet()
    
    print(f'Data transforming...')
    for old_sheet_name in old_sheets:
        print(f"DataFrame of old sheet '{old_sheet_name}':")
        old_sheet_df = pd.read_excel(old_sheet_name)
        print(old_sheet_df.head())  # Print DataFrame of old sheet before transformation
        final_data = fm.dataTransformation()
        if final_data is not None:
            fm.delNaN('Status')
            fm.delNaN('Comment')
            final_data.to_excel(new_sheet, index=False, engine='openpyxl')
            print(f"Transformation completed and saved to '{new_sheet}'.")
            print(f"DataFrame of new sheet:")
            print(final_data.head())  # Print DataFrame of new sheet
        else:
            print("Transformation failed.")


