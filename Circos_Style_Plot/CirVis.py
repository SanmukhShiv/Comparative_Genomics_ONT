import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

# Define the input directory path
input_directory = '/home/w78998ss/Visualization_Data/Circular_Plots/All_CirVis'

# Define the schemes with the desired order
schemes = [
    {
        'name': 'BY4741_synV',
        'circumference_color': 'yellow',
        'scaffolded_assemblies': [
            {
                'name': 'Scaff_R6',
                'data_file': 'rear_filtered_LUs5_x_refdbR6_df.txt_data.csv'
            }
        ]
    },
    {
        'name': 'BY4741_synII_III',
        'circumference_color': 'yellow',
        'scaffolded_assemblies': [
            {
                'name': 'Scaff_008',
                'data_file': 'rear_filtered_LUs2,3_x_refdb008_df.txt_data.csv'
            },
            {
                'name': 'Scaff_009',
                'data_file': 'rear_filtered_LUs2,3_x_refdb009_df.txt_data.csv'
            },
            {
                'name': 'Scaff_010',
                'data_file': 'rear_filtered_LUs2,3_x_refdb010_df.txt_data.csv'
            }
        ]
    },
    {
        'name': 'BY4741_synIII_VI_IXR',
        'circumference_color': 'yellow',
        'scaffolded_assemblies': [
            {
                'name': 'Scaff_012',
                'data_file': 'rear_filtered_LUs3,6,9R_x_refdb012_df.txt_data.csv'
            },
            {
                'name': 'Scaff_013',
                'data_file': 'rear_filtered_LUs3,6,9R_x_refdb013_df.txt_data.csv'
            },
            {
                'name': 'Scaff_014',
                'data_file': 'rear_filtered_LUs3,6,9R_x_refdb014_df.txt_data.csv'
            },
            {
                'name': 'Scaff_015',
                'data_file': 'rear_filtered_LUs3,6,9R_x_refdb015_df.txt_data.csv'
            }
        ]
    },
    {
        'name': 'BY4741_synIXR',
        'circumference_color': 'yellow',
        'scaffolded_assemblies': [
            {
                'name': 'Scaff_004',
                'data_file': 'rear_filtered_LUs9R_x_refdb004_df.txt_data.csv'
            },
            {
                'name': 'Scaff_005',
                'data_file': 'rear_filtered_LUs9R_x_refdb005_df.txt_data.csv'
            },
            {
                'name': 'Scaff_006',
                'data_file': 'rear_filtered_LUs9R_x_refdb006_df.txt_data.csv'
            },
            {
                'name': 'Scaff_007',
                'data_file': 'rear_filtered_LUs9R_x_refdb007_df.txt_data.csv'
            }
        ]
    }
]

# Create a larger figure and axis for your Circos-style plot
fig, ax = plt.subplots(figsize=(20, 20))
ax.set_aspect('equal')  # Ensure a circular plot

# Define colors for rearrangement types
rearrangement_colors = {
    'Insertion': 'blue',
    'Duplication': 'green',
    'Translocation': 'red',
    'Deletion': 'orange',
    'Inversion': 'cyan',
    'Tandem Duplication': 'brown'
}

# Define the arrow's properties (length, width, etc.)
arrow_length = 0.01
arrow_width = 0.01

# Create legend handles and labels with colored boxes and event counts
legend_handles = []
legend_labels = []

# Create a dictionary to store event counts
event_counts = {}

# Initialize radii for yellow and purple circles
yellow_radius = 0.4
purple_radius = 0.45  # Start with a larger purple_radius for the innermost circle

# Iterate through each scheme
for scheme in schemes:
    reference_genome = scheme['name']
    reference_circumference_color = scheme['circumference_color']
    scaffolded_assemblies = scheme['scaffolded_assemblies']

    # Plot yellow circumference for the reference genome
    circle_reference = plt.Circle((0, 0), yellow_radius, color=reference_circumference_color, fill=False, lw=4)
    ax.add_artist(circle_reference)

    # Plot purple circumferences for scaffolded assemblies and colored arrows for rearrangements
    for scaffolded_assembly in scaffolded_assemblies:
        scaffold_name = scaffolded_assembly['name']
        data_file = scaffolded_assembly['data_file']

        # Plot colored arrows for rearrangements
        df = pd.read_csv(os.path.join(input_directory, data_file))

        for index, row in df.iterrows():
            rearrangement_type = row['Rearrangement Type']
            query_start = row['Query Start']
            query_end = row['Query End']
            subject_start = row['Subject Start']
            subject_end = row['Subject End']

            color = rearrangement_colors.get(rearrangement_type, 'gray')

            angle = np.deg2rad((query_start + query_end) / 2)

            x_arrow = np.cos(angle) * purple_radius
            y_arrow = np.sin(angle) * purple_radius

            ax.arrow(x_arrow, y_arrow, np.cos(angle) * arrow_length, np.sin(angle) * arrow_length,
                     color=color, width=arrow_width, head_width=2 * arrow_width)

            if rearrangement_type not in event_counts:
                event_counts[rearrangement_type] = 1
            else:
                event_counts[rearrangement_type] += 1

        # Purple circumference for scaffolded assembly (move this part here)
        circle_scaffold = plt.Circle((0, 0), purple_radius, color='purple', fill=False, lw=4)
        ax.add_artist(circle_scaffold)

        # Increment radii for the next scaffolded assembly
        yellow_radius += 0.1
        purple_radius += 0.1  # Increase the purple_radius for the next circle

# Create legend labels with colored boxes and event counts
for event_type, count in event_counts.items():
    legend_label = f'{event_type} ({count})'
    legend_labels.append(legend_label)
    legend_handles.append(Patch(color=rearrangement_colors.get(event_type, 'gray'), label=legend_label))

# Set plot limits, remove ticks, and add labels
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_xticks([])
ax.set_yticks([])

# Add labels for the inner circles
for i, scheme in enumerate(schemes):
    ax.annotate(scheme['name'], xy=(0, 0.35 + i * 0.2), ha='center', va='center', weight='bold', fontsize=14)

# Add a color legend outside the plot area and make it 5 times bigger
legend = ax.legend(handles=legend_handles, loc='upper right', title='Rearrangement Type',
                   bbox_to_anchor=(1.05, 1), fontsize=24, title_fontsize=22)
for text in legend.get_texts():
    text.set_color('black')

# Add title to the plot
ax.set_title('A Comparative Visualization of the LoxP Rearrangements in Multiple Yeast Genomes',
             fontsize=24, weight='bold')

# Save the plot to the specified output file path
output_file_path = '/home/w78998ss/Visualization_Data/Circular_Plots/All_CirVis/All_CirVis.png'
plt.savefig(output_file_path, dpi=300, bbox_inches='tight')

# Display the plot
plt.show()
