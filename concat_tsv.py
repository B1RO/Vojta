import os
import pandas as pd

# Set the path to the folder containing the TSV files
folder_path = "./compounds"

# Get a list of all TSV files in the folder
file_list = [file for file in os.listdir(folder_path) if file.endswith(".tsv")]

# Initialize an empty DataFrame to store the concatenated data
concatenated_data = pd.DataFrame()

# Concatenate the data from each TSV file
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    try:
        data = pd.read_csv(file_path, sep="\t")
        if not data.empty:
            concatenated_data = pd.concat([concatenated_data, data], ignore_index=True)
            print(f"File {file_name} processed successfully.")
        else:
            print(f"File {file_name} is empty. Skipping.")
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as e:
        print(f"Error processing file {file_name}: {e}")

# Save the concatenated data to a new TSV file
output_file_path = os.path.join(folder_path, "concatenated_data.tsv")
concatenated_data.to_csv(output_file_path, sep="\t", index=False)

print("Concatenation complete. The output file 'concatenated_data.tsv' has been created.")
