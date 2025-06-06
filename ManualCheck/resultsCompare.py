import pandas as pd
import matplotlib.pyplot as plt

# Load both CSV files
file1 = pd.read_csv('results-50-40-30-fullAll.csv')  # Replace with actual path
file2 = pd.read_csv('Patches-kafka-linked-2022-06-02--2025-04-15.csv')  # Replace with actual path

# Extract relevant columns
df1 = file1[['Pr nr', 'Patch classification']].copy()
df2 = file2[['Pr nr', 'Patch classification']].copy()

# Rename columns for clarity before merging
df1.columns = ['Pr nr', 'GACPD']
df2.columns = ['Pr nr', 'Pareco']

# Merge on 'Pr nr'
merged = pd.merge(df1, df2, on='Pr nr', how='inner')

# Find mismatches
# Filter mismatches: exclude where both are NaN and include only actual differences
diffs = merged[
    ~((merged['GACPD'].isna()) & (merged['Pareco'].isna())) &
    (merged['GACPD'] != merged['Pareco'])
]

ccToNA = 0
ccToMO = 0
ccToED = 0
ccToSP = 0
ccToNE = 0

naToSP = 0
naToED = 0
naToMO = 0
naToCC = 0
naToNE = 0

otherChanges = 0

print(f"Total Differences: {len(diffs)}")

for index, row in diffs.iterrows():
    pr_number = row['Pr nr']
    gacpd_class = row['GACPD']
    pareco_class = row['Pareco']

    if pd.isna(gacpd_class) and pareco_class == 'CC':
        ccToNA += 1
    elif gacpd_class == 'MO' and pareco_class == 'CC':
        ccToMO += 1
    elif gacpd_class == 'ED' and pareco_class == 'CC':
        ccToED += 1
    elif gacpd_class == 'SP' and pareco_class == 'CC':
        ccToSP += 1
    elif gacpd_class == 'NE' and pareco_class == 'CC':
        ccToNE += 1
    elif gacpd_class == 'SP' and pd.isna(pareco_class) :
        naToSP += 1
    elif gacpd_class == 'ED' and pd.isna(pareco_class) :
        naToED += 1
    elif gacpd_class == 'MO' and pd.isna(pareco_class) :
        naToMO += 1
    elif gacpd_class == 'CC' and pd.isna(pareco_class) :
        naToCC += 1
    elif gacpd_class == 'NE' and pd.isna(pareco_class) :
        naToNE += 1
    elif pareco_class == 'SP' and pd.isna(gacpd_class):
        naToSP += 1
    elif pareco_class == 'ED' and pd.isna(gacpd_class):
        naToED += 1
    elif pareco_class == 'MO' and pd.isna(gacpd_class):
        naToMO += 1
    elif pareco_class == 'CC' and pd.isna(gacpd_class):
        naToCC += 1
    elif pareco_class == 'NE' and pd.isna(gacpd_class):
        naToNE += 1
    elif not pd.isna(gacpd_class)  and not pd.isna(pareco_class):
        otherChanges += 1

print(f"ccToNA: {ccToNA}")
print(f"ccToMO: {ccToMO}")
print(f"ccToED: {ccToED}")
print(f"ccToSP: {ccToSP}")
print(f"ccToNE: {ccToNE}")
print("=====================")
print(f"naToSP: {naToSP}")
print(f"naToED: {naToED}")
print(f"naToMO: {naToMO}")
print(f"naToCC: {naToCC}")
print(f"naToNE: {naToNE}")
print("=====================")
print(f"otherChanges: {otherChanges}")
print(f"Total Calculations: {ccToNA+ccToMO+ccToED+ccToSP+naToSP+ccToNE+naToED+naToMO+naToCC+naToNE+otherChanges}")

counts = {
    "ccToNA": ccToNA,
    "ccToMO": ccToMO,
    "ccToED": ccToED,
    "ccToSP": ccToSP,
    "ccToNE": ccToNE,
    "naToSP": naToSP,
    "naToED": naToED,
    "naToMO": naToMO,
    "naToCC": naToCC,
    "naToNE": naToNE,
    "otherChanges": otherChanges
}

# Plotting
plt.figure(figsize=(12, 6))
plt.bar(counts.keys(), counts.values())
plt.title("Patch Classification Changes")
plt.xlabel("Change Type")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y')

# Display the plot
plt.show()

# Save mismatches to a new CSV
output_path = 'classification_mismatches.csv'
diffs.to_csv(output_path, index=False)

print(f"Mismatches saved to: {output_path}")
