import pandas as pd
import os
import re
from functools import reduce


class CSVHandler:
    def __init__(self, directory_path, league_name):
        self.directory_path = directory_path
        self.league_name = league_name

    def clean_team_name(self, team_name):
        """Remove numbers and special characters from team names."""
        return re.sub(r'\d+\.', '', team_name).strip()

    def load_and_prepare_csv(self, file_path, prefix):
        """Load a CSV and prefix its columns with the filename and original column name."""
        df = pd.read_csv(file_path)
        df.rename(columns=lambda x: f"{prefix}_{x}" if x != 'Team' else x, inplace=True)
        return df

    def aggregate_csv_data(self, file_paths_with_prefixes):
        """Aggregate multiple CSV files by 'Team' after prefixing their columns."""
        prepared_dfs = [self.load_and_prepare_csv(file_path, prefix) for file_path, prefix in file_paths_with_prefixes]
        final_df = reduce(lambda left, right: pd.merge(left, right, on='Team', how='outer'), prepared_dfs)
        final_df['Team'] = final_df['Team'].apply(self.clean_team_name)
        aggregated_df = final_df.groupby('Team').agg(
            lambda x: ', '.join(x.dropna().astype(str).unique()) if x.dtype == 'object' else x.mean()
        )
        return aggregated_df.reset_index()

    def list_csv_files_in_directory(self):
        """List all CSV files in the given directory."""
        return [os.path.join(self.directory_path, file) for file in os.listdir(self.directory_path) if
                file.endswith('.csv')]

    def process_csv_directory(self):
        """Process a directory of CSVs and aggregate them into a single dataframe."""
        csv_files = self.list_csv_files_in_directory()
        prefixes = [os.path.basename(csv).replace(f'_{self.league_name}.csv', '') for csv in csv_files]
        files_with_prefixes = list(zip(csv_files, prefixes))
        aggregated_csv_dataset = self.aggregate_csv_data(files_with_prefixes)

        # Filtra colunas para remover quaisquer uma com 'Overall' ou 'Rating' em seus nomes
        columns_to_stay = [col for col in aggregated_csv_dataset.columns if
                           'Overall' not in col and 'Rating' not in col and 'assists' not in col
                           and 'Detailed_saves' not in col and 'Detailed_goals' not in col and 'Detailed_fouls' not in col
                           and 'Detailed_shots' not in col and 'Detailed_interception' not in col and '_Discipline' not in col
                           and 'Detailed_aerial' not in col]

        aggregated_dataset_filtered = aggregated_csv_dataset[columns_to_stay]

        columns_to_remove = ['Detailed_tackles_Away_TotalTackles', 'Detailed_tackles_Home_TotalTackles',
                             'Detailed_dribbles_Away_Total Dribbles', 'Detailed_dribbles_Home_Total Dribbles',
                             'Shot Directions - Against_Away_R', 'Shot Zones - Against_Home_R',
                             'Shot Directions - Against_Away_R',
                             'Shot Zones - Against_Home_R', 'Action Zones_Away_R', 'Attack Sides_Home_R',
                             'Shot Directions - For_Home_R',
                             'Attack Sides_Away_R', 'Shot Directions - For_Away_R', 'Shot Zones - For_Home_R',
                             'Shot Zones - For_Away_R',
                             'Shot Directions - Against_Home_R', 'Action Zones_Home_R', 'Shot Zones - Against_Away_R']

        aggregated_dataset_filtered = aggregated_dataset_filtered.drop(columns_to_remove, axis=1)

        output_csv_path = f"/home/leviatan/Documentos/league-data/aggregated_dataset_{self.league_name}.csv"  # Replace with your desired output path
        aggregated_dataset_filtered.to_csv(output_csv_path, index=False)