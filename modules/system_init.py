import os
import yaml
import re

def update_metadata(path: str, field: str, value: str) -> None:
    with open(path, 'r') as file:
        content = file.read()
    metadata_pattern = re.compile(r'^---\n(.*?)\n---', re.DOTALL | re.MULTILINE)
    metadata_match = metadata_pattern.match(content)

    if metadata_match:
        current_metadata = yaml.load(metadata_match.group(1), Loader=yaml.SafeLoader)
        current_metadata[field] = value
        updated_metadata = yaml.dump(current_metadata)
        updated_content = f"---\n{updated_metadata}---{content[metadata_match.end():]}"
    else:
        metadata = {
            field: value
        }
        yaml_metadata = yaml.dump(metadata)
        updated_content = f"---\n{yaml_metadata}\n---{content}"

    with open(path, 'w') as file:
        file.write(updated_content)

def init():
    # initialize zettelkasten in current directory
    current_directory = os.getcwd()
    md_exists = any(file.endswith(".md") for file in os.listdir(current_directory))

    registers = ['.notes-register', '.references-register', '.projects-register']
    markdowns = [file for file in os.listdir(current_directory) if file.endswith(".md")]
    file_type = {1:"note", 2:"reference", 3:"project"}

    for register in registers:
        os.makedirs(os.path.join(current_directory, register), exist_ok=True)
        with open(os.path.join(current_directory, register, 'bibliography.md'), 'w') as bibliography:
            bibliography.write("# Bibliography\n")

    if md_exists:
        manual = True if input("Manually class each .md file?(y/n)") == "y" else False
        if manual == True:
            for markdown in markdowns:
                print(f"Class the file '{markdown}' as:")
                print("1. Note")
                print("2. Reference")
                print("3. Project")
                choice = int(input("(1/2/3)"))

                while choice not in [1, 2, 3]:
                   print("Enter 1, 2, or 3")
                   choice = int(input("(1/2/3)"))

                update_metadata(os.path.join(current_directory, markdown), "type", file_type[choice])
        update()

def update():
    print("Hello world")


            
