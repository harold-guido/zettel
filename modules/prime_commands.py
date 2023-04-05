import os
import yaml
import re
from .markdown import Markdown

# declaring variables used throughout module
REGISTERS = ['', '.notes-register', '.references-register', '.projects-register']
FILE_TYPES = ['Note', 'Reference', 'Project']

def update_metadata(path: str, field: str, value: str) -> None:
    metadata_pattern = re.compile(r'^---\n(.*?)\n---', re.DOTALL | re.MULTILINE)
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

# def find_markdowns(directory):
#     # creates a dictionary of key: value pairs
#     # key = root of files
#     # value = list of .md files within directory that are not .bibliography files
#     # ignores .directories
#
#     root_markdowns={}
#     sub_directories = [dir[0] for dir in os.walk(directory)]
#                        # if not dir[0].endswith(f"{directory}")]
#     for sub_directory in sub_directories:
#         markdowns = [file for file in os.listdir(sub_directory) 
#                      if file.endswith(".md") and (file != "Bibliography.md" and file != "bibliography.md")]
#
#         root_markdowns.update({sub_directory: markdowns})
#
#     return root_markdowns

def find_markdowns(directory_path):
    # returns list of Markdown objects based on find_markdowns_paths
    markdowns = []
    markdown_paths = find_markdowns_paths(directory_path)
    for path in markdown_paths:
        markdowns.append(Markdown(path))
    return markdowns

def find_markdowns_paths(directory_path):
    # returns a list of markdown paths within directory - includes paths nested in subdirectories
    dir_markdowns = []
    subdir_markdowns = []
    with os.scandir(directory_path) as entries:
        for entry in entries:
            if not entry.name.startswith('.') and entry.is_dir():
                subdir_markdowns = subdir_markdowns + find_markdowns_paths(entry.path)
            elif not entry.name.startswith('.') and entry.name.endswith('.md'):
                dir_markdowns.append(entry.path)
        if len(subdir_markdowns) == 0:
            return dir_markdowns
        else:
            return dir_markdowns + subdir_markdowns

def init():
    # initialize zettelkasten in current directory
    current_directory = os.getcwd()
    markdowns = find_markdowns(current_directory)

    # create hidden register
    # use only one register to store all other bibliographies
    os.makedirs(os.path.join(current_directory, ".register"), exist_ok=True)
    # init does not make bibliography files

    print(markdown.name for markdown in markdowns)
    # print("\n".join([markdown.name for markdown in markdowns]))
    manual = True if input(f"There are {len(markdowns)} .md files in directory.\nManually class each file?(y/n)") == "y" else False

    for markdown in markdowns:
        if manual == True:
            print(f"Class the file '{markdown.name}' as:")
            type_index = 1
            for file_type in FILE_TYPES:
                print(f"{type_index}. {file_type}")
                type_index += 1
            choice = int(input("Choose: " + "/".join([str(n+1) for n in range(type_index-1)]) + "\n"))

            # while int(input("Choose: " + "/".join([str(n+1) for n in range(type_index)]))) not in range(type_index+1):
            #     print("Not a valid option")

            markdown.type_name = FILE_TYPES[choice - 1]
        else:
            # default type
            markdown.type_name = "Note"


    # for root in markdowns:
    #     for markdown in markdowns.get(root):
    #         if manual == True:
    #             print(f"Class the file '{markdown}' as:")
    #             print("1. Note")
    #             print("2. Reference")
    #             print("3. Project")
    #             choice = int(input("(1/2/3)"))
    #
    #             while choice not in [1, 2, 3]:
    #                print("Enter 1, 2, or 3")
    #                choice = int(input("(1/2/3)"))
    #
    #             update_metadata(os.path.join(root, markdown), "type", FILE_TYPES[choice])
    #         else:
    #             update_metadata(os.path.join(root, markdown), "type", "note")
    update()

def get_links(path):
    with open(path, 'r') as file:
        content = file.read()

    # match the path string inside of each link
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)', re.MULTILINE)
    # get list of paths
    links = link_pattern.findall(content)
    # remove duplicates
    links = list(dict.fromkeys(links))
    file_links = []
    broken_file_links = []

    for path in links:
        # check if link is to an existing file
        if os.path.isfile(path):
            file_links.append(path)
        elif not os.path.isfile(path) and os.path.isdir(os.path.dirname(path)):
            file_links.append(path)
            broken_file_links.append(path)

    return [file_links, broken_file_links]

def draw_tree(links):
    
    return("Hello World")
    # draws file tree diagram of link structure within each bibliography

def update(markdowns={}, current_directory=os.getcwd()):
    print('runs update')

    # update metadata: type, links, backlinks using yaml

    # create dictionary in format:
    # links = {name: {links:[], backlinks:[]}}
    links = {}

    # NOTE: It is at least the user's responsibility to use [link](./filename)
    # NOTE: For now user has to write link paths relative to root directory of zettel
    # NOTE: Relative paths in format
    # NOTE: ./file or ./dir/dir/.../file

    # first go through each markdown file and collect links in format []()
    markdowns = find_markdowns(current_directory) if markdowns != find_markdowns(current_directory) else markdowns

    for root in markdowns:
        # populate front links of links dict
        for markdown in markdowns.get(root):
            links.update({ os.path.join(root, markdown):{ 
                # get front links in format [[link paths],[broken or todo links]]
                'front_links': get_links(os.path.join(root, markdown)), 'back_links': []}})

    # notify user of potentially broken or uncompleted links

    # populate backlinks
    # use os.path.samefile(path1, path2)

    for markdown_path_reference in links:
        for markdown_path_check in links:
            if markdown_path_reference != markdown_path_check:
                for file_path in links.get(markdown_path_check).get('front_links')[0]:
                    if file_path not in links.get(markdown_path_check).get('front_links')[1]:
                        if os.path.samefile(markdown_path_reference, file_path):
                            links.get(markdown_path_reference).get('back_links').append(markdown_path_check)

    # using os.path.basename(path)
    draw_tree(links)

    # loop through links[name] and for each link add the corresponding backlink to file if it exists
    # if file does not exist add link name to a links["to-do"]

    # create draw_tree() function to create a tree based on links and backlinks
