# Comparative_Genomics_ONT 
The scripts/commands are in the respectively named folders and can be executed in a conda environment using specified packages. The basic chronology to be adopted for
generating results is : 
1. Correction & Scaffoldin of de novo assemblies.
2. Using Bandage software to visualize the de novo assemblies.
3. Using scaffolded assemblies to create databases for BLASTN.
4. Performing BLASTN using the LoxP sites as queries.
5. Filtering the result dataframes & assingning rearrangement events.
6. Using QUAST tool and generating MultiQC report.
7. Creating plots with LoxP rearrangements represented as coloured triangles.
8. Creating Circos-style plot to depict the rearrangement events in all the yeast genomes in the project.
9. Performing multiple sequence alignment using "Mugsy" and viewing results in Jalview Software. 
