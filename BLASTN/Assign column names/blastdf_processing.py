import os
import pandas as pd

# Column names for the DataFrame
column_names = [
    "Query Sequence", "Subject Sequence", "% Identity", "Alignment Length", "Mismatches",
    "Gap Openings", "Query Start", "Query End", "Subject Start", "Subject End", "E-value", "Bit Score"
]

# List of file names
file_names = [
    "LUs9R_x_refdb004.txt", "LUs9R_x_refdb005.txt", "LUs9R_x_refdb006.txt", "LUs9R_x_refdb007.txt",
    "LUs2,3_x_refdb008.txt", "LUs2,3_x_refdb009.txt", "LUs2,3_x_refdb010.txt",
    "LUs3,6,9R_x_refdb012.txt", "LUs3,6,9R_x_refdb013.txt", "LUs3,6,9R_x_refdb014.txt", "LUs3,6,9R_x_refdb015.txt",
    "LUs5_x_refdbR6.txt"
]

# Create a directory to store output files
output_directory = "Bprocessed_Data"
os.makedirs(output_directory, exist_ok=True)

# Iterate through the file names
for file_name in file_names:
    # Read BLASTN results from the text file
    with open(file_name, 'r') as file:
        blastn_results = [line.strip().split('\t') for line in file]

    # Create a Pandas DataFrame with the data and column names
    blastn_df = pd.DataFrame(blastn_results, columns=column_names)
    
    # Extract the file name (without extension) for the output file
    output_file_name = os.path.splitext(os.path.basename(file_name))[0]
    
    # Define the output file path
    output_file_path = os.path.join(output_directory, f"{output_file_name}_df.txt")
    
    # Save the DataFrame as a tab-separated .txt file
    blastn_df.to_csv(output_file_path, sep='\t', index=False)

# Display a message when the process is complete
print("DataFrames saved as .txt files in the output directory.")
