import os
import pandas as pd
import shutil
import subprocess

GACPD_Files = []
Pareco_Files = []

def process_csv_files(file1_path, file2_path, file3_path, output_dir):
    # Load the CSV files into DataFrames
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)
    df3 = pd.read_csv(file3_path)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get the unique Pr_nr values from file3
    valid_pr_nr = set(df3['Pr nr'])

    # Find unique Pr_nr present in both df1 and df2
    unique_pr_nr = set(df1['Pr nr']).union(set(df2['Pr nr'])).intersection(valid_pr_nr)

    for pr_nr in unique_pr_nr:
        # Filter rows for the current Pr_nr
        df1_filtered = df1[df1['Pr nr'] == pr_nr]
        df2_filtered = df2[df2['Pr nr'] == pr_nr]

        # Merge on 'Pr nr' and 'Filenames' to compare 'File classification'
        merged_df = pd.merge(df1_filtered, df2_filtered, on=['Pr nr', 'Filename'], suffixes=('_df1', '_df2'))

        # Consider NaN (empty) values as equal
        differing_rows = merged_df[
            (merged_df['File classification_df1'].fillna('') != merged_df['File classification_df2'].fillna(''))]

        # old check: pr_nr == 12859 -> not differing_rows.empty
        if pr_nr == 12859:
            folder_path = output_dir
            os.makedirs(folder_path, exist_ok=True)

            # Save the filtered differing rows
            df1_diff = df1_filtered[df1_filtered['Filename'].isin(differing_rows['Filename'])]
            df2_diff = df2_filtered[df2_filtered['Filename'].isin(differing_rows['Filename'])]

            if not (df1_diff.empty and df2_diff.empty):
                if not df1_diff.empty:
                    df1_diff.to_csv(os.path.join(folder_path, f"fileGACPD_{pr_nr}.csv"), index=False)
                    GACPD_Files.append(f"fileGACPD_{pr_nr}.csv")
                if not df2_diff.empty:
                    df2_diff.to_csv(os.path.join(folder_path, f"filePARECO_{pr_nr}.csv"), index=False)
                    Pareco_Files.append(f"filePARECO_{pr_nr}.csv")

def remove_all_files(directory_path):
    # Check if the directory exists
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        # Loop through all files and directories in the specified directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                # Remove file if it's a file, or recursively delete if it's a directory
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print("The specified directory does not exist or is not a directory.")


def start_manual_automatic_check(folder):
    j = 0
    for file in GACPD_Files:
        df1 = pd.read_csv(f"{folder}/{file}")
        df2 = pd.read_csv(f"{folder}/{Pareco_Files[j]}")
        j += 1
        for i in range(0, len(df1['Filename'])):
            filePatch = df1['Filename'][i].split('.')
            filename = filePatch[0].split("/")
            filename = filename[len(filename)-1]+".patch"

            print("***********************")
            print(f"Currently checking: {filename} in PR:{str(df1['Pr nr'][i])}")
            print(f"Pareco: {df2['File classification'][i]} GACPD: {df1['File classification'][i]}")
            print(f"Full path: {df1['Filename'][i]}")
            print("***********************")

            shutil.copy("../Results/Repos_files/1/"+df1['Mainline'][i]+"/"+str(df1['Pr nr'][i])+"/patches/"+filePatch[0]+".patch",
                        "src")
            shutil.copy(
                "../Results/Repos_files/1/" + df1['Fork'][i] + "/" + df1['Filename'][i],
                "cmp")

            subprocess.run([
                "python", "checks.py", f'src/{filename}', "src", filePatch[1]
            ])

            subprocess.run(
                ['jscpd', '--pattern', f'*.{filePatch[1]}'])

            save = input("Click Enter to continue: ")

            if save:
                remove_all_files('src')
                remove_all_files('cmp')
                remove_all_files('reports')
                print()

# Example usage
file1_path = 'GACPD-50-40-30-new.csv'
file2_path = 'test-3.csv'
file3_path = 'differences-50-40-30-new.csv'
output_dir = 'Jan27_50Checks'

remove_all_files('src')
remove_all_files('cmp')
remove_all_files('reports')
remove_all_files('Jan27_50Checks')

process_csv_files(file1_path, file2_path, file3_path, output_dir)
start_manual_automatic_check(output_dir)
