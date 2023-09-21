import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from Bio import SeqIO

# Define the new directory path
directory_path = '/home/w78998ss/Visualization_Data/ArrowsPlot/Ref_Syn3,6,9R'

# Read the new reference genome with a custom key function
new_reference_genome_path = os.path.join(directory_path, 'BY4741_synIII_VI_IXR.fa')
unique_identifier_counter = {}  # Dictionary to track unique identifiers

# Function to handle duplicate identifiers by generating unique keys
def custom_key_function(title):
    identifier = title.split()[0]  # Use the first part of the title as the identifier
    if identifier not in unique_identifier_counter:
        unique_identifier_counter[identifier] = 1
    else:
        unique_identifier_counter[identifier] += 1
        identifier = f"{identifier}_{unique_identifier_counter[identifier]}"
    return identifier

# Read the new reference genome with a custom key function
new_reference_genome = list(SeqIO.parse(new_reference_genome_path, 'fasta'))

# Check if there is at least one sequence in the reference genome
if not new_reference_genome:
    raise ValueError("There are no sequences in the reference genome.")

# Select the first sequence as the reference sequence
new_reference_sequence = new_reference_genome[0].seq

# Define the paths for scaffolded assemblies for Syn3,6,9R
new_scaffolded_assembly_paths = [
    os.path.join(directory_path, 'ragtag.scaffold_012.fasta'),
    os.path.join(directory_path, 'ragtag.scaffold_013.fasta'),
    os.path.join(directory_path, 'ragtag.scaffold_014.fasta'),
    os.path.join(directory_path, 'ragtag.scaffold_015.fasta')
]

# Define the paths for rearrangement data CSV files for Syn3,6,9R
new_rearrangement_data_paths = [
    os.path.join(directory_path, 'rear_filtered_LUs3,6,9R_x_refdb012_df.txt_data.csv'),
    os.path.join(directory_path, 'rear_filtered_LUs3,6,9R_x_refdb013_df.txt_data.csv'),
    os.path.join(directory_path, 'rear_filtered_LUs3,6,9R_x_refdb014_df.txt_data.csv'),
    os.path.join(directory_path, 'rear_filtered_LUs3,6,9R_x_refdb015_df.txt_data.csv')
]

# Create lists to store scaffolded assembly data
scaffolded_assemblies = []
scaffolded_assembly_labels = ['Scaff_012', 'Scaff_013', 'Scaff_014', 'Scaff_015']

# Read and store scaffolded assemblies
for scaffolded_assembly_path in new_scaffolded_assembly_paths:
    scaffolded_assembly_records = list(SeqIO.parse(scaffolded_assembly_path, 'fasta'))
    scaffolded_assembly = scaffolded_assembly_records[0]
    scaffolded_assemblies.append(scaffolded_assembly)

# Calculate the maximum scaffolded assembly length
max_scaffolded_len = max(len(sa) for sa in scaffolded_assemblies)

# Set the reference length and scaffolded length to match the maximum scaffolded assembly length
reference_len = max_scaffolded_len
scaffolded_len = max_scaffolded_len

# Create a figure and axis with adjusted size
fig, ax = plt.subplots(figsize=(12, 6))

# Plot reference genome as a yellow line
reference_line, = ax.plot([0, reference_len], [0] * 2, color='yellow', linewidth=5, label='Reference Genome (BY4741_synIII_VI_IXR)')

# Define the color scheme for rearrangement types
color_scheme = {
    'Insertion': 'purple',
    'Duplication': 'blue',
    'Translocation': 'green',
    'Deletion': 'red',
    'Inversion': 'cyan',
    'Circularization': 'pink'
}

# Use seaborn's color palette to assign colors based on the scheme
palette = sns.color_palette(list(color_scheme.values()))

# Create a dictionary to store event counts for each type
event_counts = {rtype: 0 for rtype in color_scheme.keys()}

# Function to plot rearrangement events on the scaffolded assembly
def plot_rearrangement_events(scaffolded_assembly, rearrangement_data, y_offset):
    for idx, row in rearrangement_data.iterrows():
        start = row['Query Start']
        end = row['Query End']
        rearrangement_type = row['Rearrangement Type']

        # Calculate positions on the x-axis for triangles (along the scaffolded assembly)
        x = [start + (end - start) / 2 + max_scaffolded_len / len(rearrangement_data) * idx]

        # Set the y position to a value corresponding to the scaffolded assembly with y_offset
        y = [y_offset]  # Position triangles on the scaffolded assembly line

        # Get the corresponding color for the rearrangement type from the palette
        color = palette[list(event_counts.keys()).index(rearrangement_type)]

        # Plot triangles
        ax.scatter(x, y, marker='^', color=color, s=200, label=None)

        # Update event counts
        event_counts[rearrangement_type] += 1

# Plot scaffolded assemblies as maroon lines and add rearrangement events
for idx, (scaffolded_assembly, label, rearrangement_data_path) in enumerate(
        zip(scaffolded_assemblies, scaffolded_assembly_labels, new_rearrangement_data_paths)
):
    ax.plot([0, scaffolded_len], [idx + 1] * 2, color='maroon', linewidth=5, label=label)

    # Read the rearrangement data for this scaffolded assembly
    rearrangement_data = pd.read_csv(rearrangement_data_path)

    # Plot rearrangement events on the scaffolded assembly
    plot_rearrangement_events(scaffolded_assembly, rearrangement_data, idx + 1)

# Set x-axis limits to match the maximum scaffolded assembly length
ax.set_xlim(0, max_scaffolded_len)

# Set x-axis label
ax.set_xlabel('Sequence Length')

# Set y-axis limits and labels
ax.set_ylim(-0.5, len(scaffolded_assemblies) + 0.5)
ax.set_yticks([i for i in range(len(scaffolded_assemblies) + 1)])
ax.set_yticklabels(['Reference Genome (BY4741_synIII_VI_IXR)', 'Scaff_012', 'Scaff_013', 'Scaff_014', 'Scaff_015'])

# Add a title
ax.set_title('Comparative Genomics Analysis with LoxP Rearrangements')

# Create a legend with colored triangles for rearrangement types and event counts
legend_elements = []

# Add legend entries for rearrangement event types and their counts
for rtype, count in event_counts.items():
    if count > 0:
        legend_elements.append(
            Line2D([0], [0], marker='^', color=color_scheme[rtype], markersize=10,
                   label=f'{rtype} ({count})', linestyle='None')
        )

# Add reference and scaffolded assembly lines to the legend
legend_elements.append(Line2D([0], [0], color='maroon', linewidth=5, label='Scaffolded Assemblies'))
legend_elements.append(Line2D([0], [0], color='yellow', linewidth=5, label='Reference Genome'))

# Create the legend outside the plot to prevent cropping
ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.25, 1))

# Save the plot in the same directory as the input files with the desired name
output_plot_path = os.path.join(directory_path, 'Arr_Syn3,6,9R.png')
plt.savefig(output_plot_path, dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
