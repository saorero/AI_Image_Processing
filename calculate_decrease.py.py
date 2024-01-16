#Code to categorize thhz lakes after finding the decrease  between the 2015 and 2016 lakes  Renamed from merge correct to calculate_decrease.py
import pandas as pd

# Read the two CSV files into DataFrames
file1 = pd.read_csv('2015Renamed.csv')
file2 = pd.read_csv('2016Renamed.csv')

# Merge the two DataFrames based on the 'Fieldname' column
merged_df = pd.merge(file1, file2, on='Filename', how='outer', suffixes=('_2015', '_2016'))

# Fill NaN values with zeros , filenames that are in 2015    but not 2016
merged_df = merged_df.fillna(0)

# Entire DataFrame to a CSV file Not grouped based on areas
#merged_df.to_csv('mergedCorrect.csv', index=False)

#CALCULATING PERCENTAGE DECREASE
merged_df['Percentage_Decrease'] = (
    (merged_df['Area_2015'] - merged_df['Area_2016']) /
    merged_df['Area_2015']
) * 100

# Filter for Lakes with Significant Decrease
mild_threshold = 20
moderate_threshold = 70

mildly_declined_lakes = merged_df[
    (merged_df['Percentage_Decrease'] > 0) & (
        merged_df['Percentage_Decrease'] <= mild_threshold)
]
moderately_declined_lakes = merged_df[
    (merged_df['Percentage_Decrease'] > mild_threshold) & (
        merged_df['Percentage_Decrease'] <= moderate_threshold)
]
severely_declined_lakes = merged_df[merged_df['Percentage_Decrease']
                                      > moderate_threshold]

# Store Results in Files
mildly_declined_lakes.to_csv('mildly_declined_lakes.csv', index=False)
moderately_declined_lakes.to_csv('moderately_declined_lakes.csv', index=False)
severely_declined_lakes.to_csv('severely_declined_lakes.csv', index=False)

