
import pandas as pd

# File paths
results_50_path = 'results-50-40-30-new.csv'  # Update with your file path
test_pareco_path = 'Pareco.csv'  # Update with your file path
output_path = 'differences-50-40-30-new.csv'

# Load data
results_50 = pd.read_csv(results_50_path)
test_pareco = pd.read_csv(test_pareco_path)

# Rename columns
results_50 = results_50.rename(columns={'Patch classification': 'GACPD'})
test_pareco = test_pareco.rename(columns={'Patch classification': 'Pareco'})

# Merge datasets to find differences
comparison = pd.merge(
    results_50[['Unnamed: 0', 'GACPD']],
    test_pareco[['Unnamed: 0', 'Pareco']],
    on='Unnamed: 0',
    how='outer',
    indicator=True
)

# Filter rows with differences
differences = comparison[comparison['_merge'] == 'both']
differences = differences[differences['GACPD'] != differences['Pareco']]

# Merge back to get additional columns
detailed_differences = pd.merge(
    differences[['Unnamed: 0', 'GACPD', 'Pareco']],
    results_50[['Unnamed: 0', 'Mainline', 'Fork', 'Pr nr']],
    on='Unnamed: 0',
    how='left'
)

# Reorder and save
detailed_differences = detailed_differences[['Unnamed: 0', 'Mainline', 'Fork', 'Pr nr', 'GACPD', 'Pareco']]
detailed_differences.to_csv(output_path, index=False)
print(f"Differences saved to {output_path}")
