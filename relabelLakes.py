#Code that assigns a unique identifier for every detected lake

import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('2016Areas.csv')

# Create a new column with the indexed values
df['Filename_Indexed'] = df.groupby('Filename').cumcount() + 1


df['Filename'] = df['Filename'] + '(' + df['Filename_Indexed'].astype(str) + ')'

# Drop the temporary index column
df = df.drop(columns=['Filename_Indexed'])

# Write the result to a new CSV file
df.to_csv('renamedFilename.csv', index=False)
