import subprocess
import os
import shutil

def obtain_git_rename_history(start_date, end_date, repo_path):
    og_path = os.getcwd()
    os.chdir(repo_path)

    # Git command to give us the oldest renames first, and then the latests
    # This ensures the dictionary will contain the most recent renames in its value
    command = [
        "git",
        "log",
        "--diff-filter=R",
        "--name-status",
        "--pretty=format:",
        f"--since={start_date}",
        f"--until={end_date}",
        "--reverse"
    ]

    results = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    rename_history = {}
    for line in results.stdout.strip().split('\n'):
        parts = line.split('\t')
        if len(parts) == 3 and parts[0].startswith("R"):
            old_name = parts[1]
            new_name = parts[2]
            if old_name in rename_history:
                rename_history[old_name].append(new_name)
            else:
                rename_history[old_name] = [new_name]

    os.chdir(og_path)

    return rename_history

def create_git_folder(repo_name):
    repo_name = repo_name.replace("\\", "/")
    repo_owner = repo_name.split("/")

    og_path = os.getcwd()
    if os.path.exists(repo_owner[0]+"/"+repo_owner[1]):
        os.chdir(repo_owner[0]+"/"+repo_owner[1])
    else:
        os.makedirs(repo_owner[0]+"/"+repo_owner[1])
        os.chdir(repo_owner[0]+"/"+repo_owner[1])

    command = [
        "git",
        "clone",
        f"https://github.com/{repo_owner[1]+"/"+repo_owner[2]}",
    ]

    subprocess.run(command)

    os.chdir(og_path)

def remove_folder(folder_name):
    folder_name = folder_name.replace("\\", "/")

    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

print("Apache/kafka Renames")

remove_folder('gitclones/apache')
create_git_folder("gitclones/apache/kafka")
renames = obtain_git_rename_history("2022-06-02", "2022-12-18", "gitclones/apache/kafka")

for filename in renames:
    print(renames[filename])

print("Linkedin/kafka Renames")
remove_folder('gitclones/linkedin')
create_git_folder("gitclones/linkedin/kafka")
renames = obtain_git_rename_history("2022-06-02", "2022-12-18", "gitclones/linkedin/kafka")

for filename in renames:
    print(renames[filename])