import subprocess
import os

# Define the directory path where your data is located
data_directory = "/home/w78998ss/Visualization_Data/QUAST"

# Define the output directory for Quast reports
output_directory = "/home/w78998ss/Visualization_Data/QUAST/quast_reps"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Define the directory for the MultiQC reports
multiqc_output_directory = "/home/w78998ss/Visualization_Data/QUAST/quast_reps/multiQC_rep"

# Create the MultiQC output directory if it doesn't exist
if not os.path.exists(multiqc_output_directory):
    os.makedirs(multiqc_output_directory)

# Define a dictionary with reference names as keys and their corresponding filenames as values
references = {
    "Reference_1_BY4741_synII_III": {
        "reference_genome": "BY4741_synII_III.fa",
        "scaffolded_assemblies": [
            "ragtag.scaffold_008.fasta",
            "ragtag.scaffold_009.fasta",
            "ragtag.scaffold_010.fasta"
        ]
    },
    "Reference_2_BY4741_synIII_VI_IXR": {
        "reference_genome": "BY4741_synIII_VI_IXR.fa",
        "scaffolded_assemblies": [
            "ragtag.scaffold_012.fasta",
            "ragtag.scaffold_013.fasta",
            "ragtag.scaffold_014.fasta",
            "ragtag.scaffold_015.fasta"
        ]
    },
    "Reference_3_BY4741_synIXR": {
        "reference_genome": "BY4741_synIXR.fa",
        "scaffolded_assemblies": [
            "ragtag.scaffold_004.fasta",
            "ragtag.scaffold_005.fasta",
            "ragtag.scaffold_006.fasta",
            "ragtag.scaffold_007.fasta"
        ]
    },
    "Reference_4_BY4741_synV": {
        "reference_genome": "BY4741_synV.fa",
        "scaffolded_assemblies": [
            "ragtag.scaffold_R6.fasta"
        ]
    }
}

# Path to the Quast executable (Quast should be installed within your Conda environment)
quast_executable = "quast"

# Path to the MultiQC executable (MultiQC should be installed within your Conda environment)
multiqc_executable = "multiqc"

# List to store the Quast report directories
quast_report_directories = []

# Loop through each reference
for reference_name, files in references.items():
    reference_genome_file = os.path.join(data_directory, files["reference_genome"])
    
    # Check if the reference genome file exists
    if os.path.isfile(reference_genome_file):
        # Generate the command to run Quast for this reference
        quast_output_dir = os.path.join(output_directory, reference_name)
        quast_command = [
            quast_executable,
            "--output-dir", quast_output_dir,
            reference_genome_file
        ]
        
        # List scaffolded assembly files for this reference
        scaffolded_assemblies = [os.path.join(data_directory, sa) for sa in files["scaffolded_assemblies"]]
        
        # Add scaffolded assembly files to the Quast command
        quast_command.extend(scaffolded_assemblies)
        
        # Run Quast for this reference
        subprocess.run(quast_command)
        
        # Store the Quast report directory for future use
        quast_report_directories.append(quast_output_dir)
    else:
        print(f"Reference genome file not found for {reference_name}")

# Execute MultiQC to create a combined report for all references
multiqc_combined_command = [multiqc_executable, output_directory, "--outdir", multiqc_output_directory]
subprocess.run(multiqc_combined_command)

# The script ends here after generating Quast and MultiQC reports.
