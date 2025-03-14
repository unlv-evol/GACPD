import openai
import os

# Your OpenAI API key
client = openai.OpenAI(api_key="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")

# Define paths
ROOT_FOLDER = "prompts/"
OUTPUT_FOLDER = "response/"

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Define initial system prompt
prompt1 = '''
From this point onward you will act as a Software Developer that has enough experience to detect Type I, Type II and Type III code clone detection.
'''

def get_chat_response(messages):
    """Send messages to OpenAI API and return the response."""
    response = client.chat.completions.create(
        model="gpt-4o",  # Use the latest model
        messages=messages
    )
    return response.choices[0].message.content


def process_file(file_path, file_name, parent_folder):
    """Process a single file independently."""
    try:
        messages = [{"role": "system", "content": prompt1}]  # Start with the first message

        # Read file content
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

        # Add file content as a user message
        messages.append({"role": "user", "content": content})

        # Send the conversation to ChatGPT
        response = get_chat_response(messages)

        # Save the response
        output_folder = os.path.join(OUTPUT_FOLDER, parent_folder)  # Keep folder structure
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, f"{file_name}_response.txt")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response)

        print(f"Processed file: {file_name}, response saved in {output_file}")
    except Exception as e:
        print("Bad happened: ", e)

def process_folders(root_folder):
    """Traverse folders and process files individually."""
    for folder, _, files in os.walk(root_folder):
        parent_folder = os.path.relpath(folder, root_folder)  # Relative path for output
        for file_name in files:
            file_path = os.path.join(folder, file_name)
            process_file(file_path, file_name, parent_folder)


if __name__ == "__main__":
    process_folders(ROOT_FOLDER)