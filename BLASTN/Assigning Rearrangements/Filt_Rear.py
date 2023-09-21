import os
import pandas as pd

# Define the list of file names
file_list = [
    "filtered_LUs2,3_x_refdb008_df.txt",
    "filtered_LUs2,3_x_refdb009_df.txt",
    "filtered_LUs2,3_x_refdb010_df.txt",
    "filtered_LUs3,6,9R_x_refdb012_df.txt",
    "filtered_LUs3,6,9R_x_refdb013_df.txt",
    "filtered_LUs3,6,9R_x_refdb014_df.txt",
    "filtered_LUs3,6,9R_x_refdb015_df.txt",
    "filtered_LUs5_x_refdbR6_df.txt",
    "filtered_LUs9R_x_refdb004_df.txt",
    "filtered_LUs9R_x_refdb005_df.txt",
    "filtered_LUs9R_x_refdb006_df.txt",
    "filtered_LUs9R_x_refdb007_df.txt"
]

# Specify the input directory path where the input files are located
input_directory = "/home/w78998ss/Blast_Data/Rearrangements/Rearg/Filt_Rearg"

# Specify the output folder path within the input directory
output_folder = os.path.join(input_directory, "Filt_Rearg_Outputs")

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Process each file
for file_name in file_list:
    # Initialize empty lists to store rearrangement data
    rearrangement_type = []
    query_start = []
    query_end = []
    subject_start = []
    subject_end = []
    alignment_length = []

    # Read the current BLAST results file with the full path
    blast_results_file = os.path.join(input_directory, file_name)
    df = pd.read_csv(blast_results_file, delimiter='\t')

    # Iterate through the dataframe rows
    for index, row in df.iterrows():
        # Extract relevant information
        query_seq = row["Query Sequence"]
        subject_seq = row["Subject Sequence"]
        alignment_len = row["Alignment Length"]
        query_start_pos = row["Query Start"]
        query_end_pos = row["Query End"]
        subject_start_pos = row["Subject Start"]
        subject_end_pos = row["Subject End"]

        # Determine rearrangement type based on alignment positions
        if query_start_pos == 1 and query_end_pos == len(query_seq):
            rearrangement_type.append("Circularization")
        elif query_start_pos == 1:
            rearrangement_type.append("Insertion")
        elif query_end_pos == len(query_seq):
            rearrangement_type.append("Deletion")
        elif query_start_pos > query_end_pos:
            rearrangement_type.append("Inversion")
        elif subject_start_pos > subject_end_pos:
            rearrangement_type.append("Translocation")
        elif query_start_pos < query_end_pos and subject_start_pos < subject_end_pos:
            rearrangement_type.append("Duplication")
        else:
            rearrangement_type.append("Other")

        # Store the extracted data
        query_start.append(query_start_pos)
        query_end.append(query_end_pos)
        subject_start.append(subject_start_pos)
        subject_end.append(subject_end_pos)
        alignment_length.append(alignment_len)

    # Create a new dataframe for rearrangement data
    rearrangement_df = pd.DataFrame({
        "Rearrangement Type": rearrangement_type,
        "Query Start": query_start,
        "Query End": query_end,
        "Subject Start": subject_start,
        "Subject End": subject_end,
        "Alignment Length": alignment_length
    })

    # Define the output file path within the "Filt_Rearg_Outputs" folder
    output_file_path = os.path.join(output_folder, f"rear_{file_name}_data.csv")

    # Export the rearrangement dataframe to the specified output file path
    rearrangement_df.to_csv(output_file_path, index=False)
