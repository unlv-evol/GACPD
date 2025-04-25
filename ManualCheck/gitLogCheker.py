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
        "--diff-filter=A",
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
        if len(parts) == 3 and parts[0].startswith("A"):
            old_name = parts[1]
            new_name = parts[2]
            if old_name not in rename_history:
                rename_history[old_name] = new_name
            else:
                print("Issue with rename history")

    os.chdir(og_path)

    return rename_history

def obtain_added_files_in_pr(head, base):
    pass

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

def find_cycle_from_file(start, renames, visited):
    path = []
    local_visited = {}

    current = start
    while current in renames:
        if current in local_visited:
            # Cycle detected
            cycle_start_idx = local_visited[current]
            cycle = path[cycle_start_idx:] + [current]
            return cycle
        if current in visited:
            return None
        local_visited[current] = len(path)
        path.append(current)
        current = renames[current]
    return None

def find_rename_cycles(renames):
    visited = set()
    cycles = []

    for file in renames:
        if file not in visited:
            cycle = find_cycle_from_file(file, renames, visited)
            if cycle:
                cycles.append(cycle)
                visited.update(cycle)

    return cycles

print("Apache/kafka Renames")

def obtained_added_files(mainline, base, head):
    pass

# remove_folder('gitclones/apache')
# create_git_folder("gitclones/apache/kafka")
renames = obtain_git_rename_history("2025-02-03T16:46:07Z", "2025-02-03T16:50:06Z","gitclones/Pokemon-Randomizer")

for filename in renames:
    print(renames[filename])

# print("Linkedin/kafka Renames")
# remove_folder('gitclones/linkedin')
# create_git_folder("gitclones/linkedin/kafka")
# renames = obtain_git_rename_history("2018-08-31", "2022-06-13", "gitclones/linkedin/kafka")

# for filename in renames:
#     print(f"OG: {filename} | New: {renames[filename]}")
#
# if 'config/self-managed/broker.properties' in renames:
#     print(f"New File name: {renames['config/self-managed/broker.properties']}")
#
# cycles = find_rename_cycles(renames)
#
# for i in range(0, len(cycles)):
#     if 'streams/src/test/java/org/apache/kafka/streams/state/internals/KeyValueSegmentIteratorTest.java' in cycles[i]:
#         print(f"Original Name is: {cycles[i][0]}")
#
# # Print cycles
# for i, cycle in enumerate(cycles, 1):
#     print(f"Cycle {i}: {cycle} (cycle starts at '{cycle[0]}')")