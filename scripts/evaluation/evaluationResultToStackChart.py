import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.colors as mcolors

# Set the directory where the CSV files are located
csv_dir = "../../evaluations/csv"

# Iterate over all CSV files in the directory
for csv_file in os.listdir(csv_dir):
    if csv_file.endswith(".csv") and csv_file.startswith("correct_answers_confidence_"):
        # Read the CSV file using Pandas
        df = pd.read_csv(os.path.join(csv_dir, csv_file))

        # Calculate the average confidence for each country
        df_mean = df.groupby('Correct_Class').mean().reset_index()

        # Calculate the percentage of correct guesses for each country
        df_count = df.groupby('Correct_Class')['Top_Guess'].apply(lambda x: x[x == True].count() / x.count()).reset_index()

        # Normalize the percentage of correct guesses to a 0-1 range
        normalized_counts = (df_count['Top_Guess'] - df_count['Top_Guess'].min()) / (df_count['Top_Guess'].max() - df_count['Top_Guess'].min())

        # Create a custom color gradient from red to lime (lighter green) based on the percentage of correct guesses
        custom_cmap = mcolors.LinearSegmentedColormap.from_list("", ["skyblue", "midnightblue"])
        colors = custom_cmap(normalized_counts)

        # Set the width of the figure proportional to the number of countries
        figure_width = max(6, len(df_mean) * 0.4)

        # Create a plot for the CSV file
        fig, ax = plt.subplots(figsize=(figure_width, 6))
        bars = ax.bar(df_mean.index, df_mean['Confidence'], label='Average Confidence Level of Correct Answer', color=colors)
        plt.xticks(df_mean.index, df_mean['Correct_Class'], rotation=90)
        plt.xlabel('Correct Answer (Country)')
        plt.ylabel('Average Confidence Level of Correct Answer')
        plt.title(f"Average Confidence Level for {csv_file.replace('.csv', '').replace('correct_answers_confidence_', '')}")
        plt.ylim(0, 1)
        plt.grid(axis='y')

        # Add a colorbar to the plot
        sm = plt.cm.ScalarMappable(cmap=custom_cmap, norm=plt.Normalize(0, 1))
        sm.set_array([])
        cbar = plt.colorbar(sm)
        cbar.set_label('Percentage of Correct Top Guesses')

        # Save the plot as an image file
        plt.savefig(f"{csv_file.replace('.csv', '')}_plot.png", bbox_inches='tight')

# Show all plots
plt.show()
