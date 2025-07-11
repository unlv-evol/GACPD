import sys
import os


def parse_patch_file(patch_file, output_dir, extension):
    with open(patch_file, 'r') as patch:
        hunk_count = 0
        add_count = 0
        del_count = 0
        additions_file = []
        deletions_file = []

        for line in patch:
            # Detect the start of a new hunk (lines starting with "@@")
            if line.startswith('@@'):
                if hunk_count >= 0:
                    save_hunk_files(hunk_count, output_dir, deletions_file, del_count, f"deletions.{extension}")
                    save_hunk_files(hunk_count, output_dir, additions_file, add_count, f"additions.{extension}")
                hunk_count += 1
                additions_file = []
                deletions_file = []

            if line.startswith('+') and not line.startswith("+++"):
                additions_file.append(line[1:])
                add_count += 1
            elif line.startswith('-') and not line.startswith("---"):
                deletions_file.append(line[1:])
                del_count += 1
            elif not line.startswith("---") and not line.startswith("+++") and not line.startswith('@@'):
                additions_file.append(line)
                deletions_file.append(line)

        # Process the last hunk if any
        if deletions_file or additions_file:
            save_hunk_files(hunk_count, output_dir, deletions_file, del_count, f"deletions.{extension}")
            save_hunk_files(hunk_count, output_dir, additions_file, add_count, f"additions.{extension}")


def save_hunk_files(hunk_id, output_dir, additions_hunks, counts, type_of_change):
    os.makedirs(output_dir, exist_ok=True)

    # Write the hunk with only additions to the additions file, if applicable
    if counts != 0:
        additions_file_path = os.path.join(output_dir, f'hunk_{hunk_id}_{type_of_change}')
        with open(additions_file_path, 'w') as add_file:
            add_file.writelines(additions_hunks)
        print(f"Saved additions file for hunk {hunk_id}: {additions_file_path}")


# Example usage
if __name__ == "__main__":
    import requests

    # GitHub API endpoint for the repository
    url = "https://api.github.com/repos/linkedin/kafka"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        created_at = data.get("created_at")
        if created_at:
            print(f"Repository created at: {created_at}")
        else:
            print("The 'created_at' field is not found in the response.")
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
    exit(0)
    if len(sys.argv) != 4:
        print("Usage: python checks.py <patch_file> <output_directory>")
        sys.exit(1)

    patch_file = sys.argv[1]
    output_dir = sys.argv[2]
    ext = sys.argv[3]

    parse_patch_file(patch_file, output_dir, ext)

