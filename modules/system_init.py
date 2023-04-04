import os
import yaml
import re

# declaring variables used throughout module
registers = ['', '.notes-register', '.references-register', '.projects-register']
metadata_pattern = re.compile(r'^---\n(.*?)\n---', re.DOTALL | re.MULTILINE)
file_type = {1:"note", 2:"reference", 3:"project"}

def update_metadata(path: str, field: str, value: str) -> None:
    # update yaml metadata
    with open(path, 'r') as file:
        content = file.read()
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

def find_markdowns(directory):
    # creates a dictionary of key: value pairs
    # key = root of files
    # value = list of .md files within directory that are not .bibliography files
    # ignores .directories

    root_markdowns={}
    sub_directories = [dir[0] for dir in os.walk(directory)]
                       # if not dir[0].endswith(f"{directory}")]
    for sub_directory in sub_directories:
        markdowns = [file for file in os.listdir(sub_directory) 
                     if file.endswith(".md") and (file != "Bibliography.md" and file != "bibliography.md")]

        root_markdowns.update({sub_directory: markdowns})

    return root_markdowns

def init():
    # initialize zettelkasten in current directory
    current_directory = os.getcwd()

    markdowns = find_markdowns(current_directory)

    for register in registers:
        os.makedirs(os.path.join(current_directory, register), exist_ok=True)
        with open(os.path.join(current_directory, register, 'Bibliography.md'), 'w') as bibliography:
            bibliography.write(f"# Bibliography{register}\n")

    manual = True if input("Manually class each .md file?(y/n)") == "y" else False
    for root in markdowns:
        for markdown in markdowns.get(root):
            if manual == True:
                print(f"Class the file '{markdown}' as:")
                print("1. Note")
                print("2. Reference")
                print("3. Project")
                choice = int(input("(1/2/3)"))

                while choice not in [1, 2, 3]:
                   print("Enter 1, 2, or 3")
                   choice = int(input("(1/2/3)"))

                update_metadata(os.path.join(root, markdown), "type", file_type[choice])
            else:
                update_metadata(os.path.join(root, markdown), "type", "note")

    update()

def update(current_directory=os.getcwd()):
    # update metadata: type, links, backlinks using yaml

    # create dictionary in format:
    # links = {name: {links:[], backlinks[]}}

    # it is at least the user's responsibility to use
    # [link](./filename) or [[filename]] as formats in their links

    # first go through each markdown file and collect links in format []() or format [[]]
    # update [[]] formatted links as []() formatted links

    # populate links[name] and links[name][links]

    # loop through links[name] and for each link add the corresponding backlink to file if it exists
    # if file does not exist add link name to a links["to-do"]

    # create make_tree() function to create a tree based on links and backlinks
    print("Hello")


    


            
