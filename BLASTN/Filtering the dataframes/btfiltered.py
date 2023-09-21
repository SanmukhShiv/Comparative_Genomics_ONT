import os
import pandas as pd

# Create the "filtered" folder if it doesn't exist
output_folder = "filtered"
os.makedirs(output_folder, exist_ok=True)

# List of file names
file_names = [
    "LUs9R_x_refdb004_df.txt", "LUs9R_x_refdb005_df.txt", "LUs9R_x_refdb006_df.txt", "LUs9R_x_refdb007_df.txt",
    "LUs2,3_x_refdb008_df.txt", "LUs2,3_x_refdb009_df.txt", "LUs2,3_x_refdb010_df.txt",
    "LUs3,6,9R_x_refdb012_df.txt", "LUs3,6,9R_x_refdb013_df.txt", "LUs3,6,9R_x_refdb014_df.txt", "LUs3,6,9R_x_refdb015_df.txt",
    "LUs5_x_refdbR6_df.txt"
]

for file_name in file_names:
    # Read the data from the current file
    data = pd.read_csv(file_name, sep="\t")
    
    # Filter rows with % identity above 95%
    filtered_data = data[data['% Identity'] > 95]
    
    # Create a new file path for the filtered data
    filtered_file_path = os.path.join(output_folder, "filtered_" + file_name)
    
    # Save the filtered data as a tab-separated text file
    filtered_data.to_csv(filtered_file_path, sep="\t", index=False)
    
    print(f"Filtered data saved as {filtered_file_path}")

