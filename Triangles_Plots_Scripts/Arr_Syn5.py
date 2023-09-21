import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from Bio import SeqIO

# Define the new directory path
directory_path = '/home/w78998ss/Visualization_Data/ArrowsPlot/Ref_Syn5/'

# Define the updated file paths using the new directory
reference_genome_path = os.path.join(directory_path, 'BY4741_synV.fa')
scaffolded_assembly_path = os.path.join(directory_path, 'ragtag.scaffold_R6.fasta')
rearrangement_data_path = os.path.join(directory_path, 'rear_filtered_LUs5_x_refdbR6_df.txt_data.csv')

# Read reference genome
reference_genome = SeqIO.index(reference_genome_path, 'fasta')

# Read scaffolded assembly as a list of records
scaffolded_assembly_records = list(SeqIO.parse(scaffolded_assembly_path, 'fasta'))
scaffolded_assembly = scaffolded_assembly_records[0]

# Read rearrangement data
rearrangement_data = pd.read_csv(rearrangement_data_path)

# Create a figure and axis with adjusted size
fig, ax = plt.subplots(figsize=(12, 6))

# Create a dictionary to store event counts for each type
event_counts = {rtype: 0 for rtype in rearrangement_data['Rearrangement Type'].unique()}

# Define the updated color scheme
color_scheme = {
    'Insertion': 'purple',
    'Duplication': 'blue',
    'Translocation': 'green',
    'Deletion': 'red',
    'Inversion': 'cyan',
    'Circularization': 'pink'
}

# Use seaborn's color palette to assign colors based on the scheme
palette = sns.color_palette([color_scheme[rtype] for rtype in event_counts.keys()])

# Plot scaffolded assembly as a maroon line
scaffolded_len = len(scaffolded_assembly)
scaffolded_line, = ax.plot([0, scaffolded_len], [1] * 2, color='maroon', linewidth=5, label='Scaffolded Assembly (Scaff_R6)')

# Plot reference genome as a yellow line
reference_len = len(reference_genome[list(reference_genome.keys())[0]])
reference_line, = ax.plot([0, reference_len], [0] * 2, color='yellow', linewidth=5, label='Reference Genome (BY4741_synV)')

# Plot loxP rearrangement events as colored triangles on the scaffolded assembly line
for idx, row in rearrangement_data.iterrows():
    start = row['Query Start']
    end = row['Query End']
    rearrangement_type = row['Rearrangement Type']

    # Calculate positions on the x-axis for triangles (along the scaffolded assembly)
    x = [start + (end - start) / 2]

    # Set the y position to a value corresponding to the scaffolded assembly
    y = [1]  # Position triangles on the scaffolded assembly line

    # Get the corresponding color for the rearrangement type from the palette
    color = palette[list(event_counts.keys()).index(rearrangement_type)]

    # Plot triangles
    ax.scatter(x, y, marker='^', color=color, s=200, label=None)

    # Update event counts
    event_counts[rearrangement_type] += 1

# Create a legend with colored triangles for rearrangement types
legend_elements = [Line2D([0], [0], marker='^', color=color_scheme[rtype], markersize=10,
                          label=f"{rtype} ({count})", linestyle='None')
                   for rtype, count in event_counts.items()]

# Add reference and scaffolded assembly lines to the legend
legend_elements.append(Line2D([0], [0], color='maroon', linewidth=5, label='Scaffolded Assembly (Scaff_R6)'))
legend_elements.append(Line2D([0], [0], color='yellow', linewidth=5, label='Reference Genome (BY4741_synV)'))

# Create the legend outside the plot to prevent cropping
ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

# Set x-axis limits and labels
ax.set_xlim(0, max(scaffolded_len, reference_len))
ax.set_xlabel('Sequence Length')

# Set y-axis limits and labels
ax.set_ylim(-0.5, 1.5)
ax.set_yticks([0, 1])
ax.set_yticklabels(['Reference Genome (BY4741_synV)', 'Scaffolded Assembly (Scaff_R6)'])

# Add a title
ax.set_title('Comparative Genomics Analysis with LoxP Rearrangements')

# Save the plot with the desired name in the same directory
output_plot_path = os.path.join(directory_path, 'Arrow_Syn5.png')
plt.savefig(output_plot_path, dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
