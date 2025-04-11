import os
import pandas as pd
import shutil
import subprocess
import openai

GACPD_Files = []
Pareco_Files = []
promp1 = "From this point onward you will act as a Software Developer that has enough experience to detect Type I, Type II and Type III code clone detection."
promp2 = '''
Through this conversation I will provide you with various code files and small code fragments. Let me be clear that by “code fragment” I mean the entire code and not the individual function. You should look for a marker called “file starters here” and “file end here” to know where the specific code fragment starts and stops. Your job will be comparing the code fragments to the code files using a token-like system. If such a case is found - you will then need to classify that code fragment as a missed opportunity (MO), effort duplication (ED), not applicable (NA) or split (SP).

If the entire code fragment consists of pure importing of libraries/external files - you should not consider that code fragment and ignore them.

Here is how we grant each of the classification:

An MO classification is granted if more tokens from the “deleted” code fragments are obtained.
An ED classification is granted if more tokens from the “added” code fragments are obtained.
An SP classification is granted if an equal number of tokens from the “deleted” and “added” code fragments is obtained.
An NA classification is granted if neither MO, ED or SP are granted.

Here is the main code file:
[Code File]

Here are all the deleted code fragments:

[Deleted Code Fragments]

Here are all the added code fragments:

[Added Code Fragments]
'''


import os
import pandas as pd

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

        # Exclude rows where 'File classification' is 'OTHER EXT' or 'ERROR'
        df1_filtered = df1_filtered[~df1_filtered['File classification'].isin(["OTHER EXT", "ERROR", "NOT EXISTING"])]
        df2_filtered = df2_filtered[~df2_filtered['File classification'].isin(["OTHER EXT", "ERROR", "NOT EXISTING"])]

        # Save the full filtered data (not just differences)
        df1_filtered.to_csv(os.path.join(output_dir, f"fileGACPD_{pr_nr}.csv"), index=False)
        GACPD_Files.append(f"fileGACPD_{pr_nr}.csv")
        df2_filtered.to_csv(os.path.join(output_dir, f"filePARECO_{pr_nr}.csv"), index=False)
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


def process_files(directory):
    processed_files = {"deleted": "", "added": ""}

    for filename in os.listdir(directory):
        if "_deletions" in filename or "_additions" in filename:
            file_path = os.path.join(directory, filename)

            # Read the file content
            with open(file_path, "r") as f:
                content = f.read()

            # Add start and end markers
            modified_content = f"File starts here\n{content}\nFile ends here"

            # Write the modified content back
            with open(file_path, "w") as f:
                f.write(modified_content)

            # Store the processed content in the dictionary
            if "_deletions" in filename:
                processed_files["deleted"] += modified_content + "\n\n"
            elif "_additions" in filename:
                processed_files["added"] += modified_content + "\n\n"

            print(f"Processed: {filename}")

    return processed_files


def insert_code_into_prompt(prompt2, code_file, deleted_fragments, added_fragments):
    """Replaces placeholders in the prompt template with actual file content."""
    prompt2 = prompt2.replace("[Code File]", code_file)
    prompt2 = prompt2.replace("[Deleted Code Fragments]", deleted_fragments)
    prompt2 = prompt2.replace("[Added Code Fragments]", added_fragments)
    return prompt2


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

            if os.path.isdir(f'prompts/{str(df1['Pr nr'][i])}') is False:
                os.makedirs(f'prompts/{str(df1['Pr nr'][i])}')

            print("***********************")
            print(f"Currently checking: {filename} in PR:{str(df1['Pr nr'][i])}")
            print(f"GACPD: {df1['File classification'][i]}")
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

            # Add automatic process here
            directory_path = 'src'

            # Process deleted and added files
            processed_fragments = process_files(directory_path)

            # Read the main code file
            main_code_file_path = os.path.join('cmp', f"{filename.split(".")[0]+"."+filePatch[1]}")  # Adjust if the filename differs
            with open(main_code_file_path, "r") as f:
                main_code_content = f.read()

            # Insert processed content into the prompt
            updated_prompt = insert_code_into_prompt(
                promp2,
                main_code_content,
                processed_fragments["deleted"],
                processed_fragments["added"]
            )

            # Save the updated prompt
            output_file = os.path.join(f'prompts/{str(df1['Pr nr'][i])}', f"updated_prompt_{filename.split(".")[0]+"."+filePatch[1]}.txt")
            with open(output_file, "w") as f:
                f.write(updated_prompt)

            print(f"Prompt updated successfully and saved to 'prompts/{str(df1['Pr nr'][i])}/updated_prompt_{filename.split(".")[0]+"."+filePatch[1]}.txt'.")

            remove_all_files('src')
            remove_all_files('cmp')
            remove_all_files('reports')
            print()

# Example usage
file1_path = '../ManualCheck/GACPD-50-40-30-new.csv'
file2_path = '../ManualCheck/test-3.csv'
file3_path = 'differences-50-40-30-new.csv'
output_dir = 'Checks'

if os.path.isdir('src') is False:
    os.makedirs('src')

if os.path.isdir('cmp') is False:
    os.makedirs('cmp')

if os.path.isdir('reports') is False:
    os.makedirs('reports')

if os.path.isdir('prompts') is False:
    os.makedirs('prompts')

remove_all_files('src')
remove_all_files('cmp')
remove_all_files('reports')
remove_all_files('prompts')
remove_all_files(output_dir)

with open("prompts/initial_prompt.txt", "w") as f:
    f.write(promp1)

process_csv_files(file1_path, file2_path, file3_path, output_dir)
start_manual_automatic_check(output_dir)
