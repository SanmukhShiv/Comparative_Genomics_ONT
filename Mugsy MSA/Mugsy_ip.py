from Bio import SeqIO
import os

def check_and_prepare_fasta_files(input_directory, output_directory):
    invalid_files = []

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    for file_name in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file_name)
        if file_name.endswith(".fasta") or file_name.endswith(".fa"):
            try:
                sequences = list(SeqIO.parse(file_path, "fasta"))

                # Check if the sequence contains only valid characters (A, C, G, T, U, N, etc.)
                if not all(set(str(record.seq).upper()).issubset("ACGTUN") for record in sequences):
                    invalid_files.append(file_name)
                    continue

                # Prepare Mugsy-ready input file by wrapping sequences to a specified line length
                output_path = os.path.join(output_directory, file_name)
                SeqIO.write(sequences, output_path, "fasta")

            except Exception as e:
                invalid_files.append(file_name)

    return invalid_files

# Input directory containing your FASTA files
input_directory = "/home/w78998ss/Visualization_Data/Mugsy"
# Output directory to store Mugsy-ready input files
output_directory = os.path.join(input_directory, "Mug_ready")

invalid_files = check_and_prepare_fasta_files(input_directory, output_directory)

if not invalid_files:
    print("All FASTA files are valid and Mugsy-ready.")
else:
    print("The following FASTA files are not valid:")
    for file_name in invalid_files:
        print(file_name)
