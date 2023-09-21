import os
import subprocess

# List of GFA files to process
file_list = [
    "assembly_graph004.gfa",
    "assembly_graph005.gfa",
    "assembly_graph006.gfa",
    "assembly_graph007.gfa",
    "assembly_graph008.gfa",
    "assembly_graph009.gfa",
    "assembly_graph010.gfa",
    "assembly_graph012.gfa",
    "assembly_graph013.gfa",
    "assembly_graph014.gfa",
    "assembly_graph015.gfa",
    "assembly_graphR6.gfa"
]

# Directory to save the output images
output_dir = "Bandage_Outputs"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through each GFA file and generate PNG images
for gfa_file in file_list:
    input_path = gfa_file
    output_path = os.path.join(output_dir, os.path.splitext(gfa_file)[0] + ".png")

    # Run the Bandage command to generate the image
    command = ["Bandage", "image", input_path, output_path]

    try:
        subprocess.run(command, check=True)
        print(f"Image generated for {gfa_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating image for {gfa_file}: {e}")
