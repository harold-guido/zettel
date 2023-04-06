import os
import yaml
import re
from .markdown import Markdown

# declaring variables used throughout module
REGISTERS = ['', '.notes-register', '.references-register', '.projects-register']
FILE_TYPES = ['Note', 'Reference', 'Project']

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
    update()

# def draw_tree(links):
#     
#     return("Hello World")

def update(markdowns=[], ):
    if len(markdowns) == 0 : markdowns=find_markdowns(os.getcwd())

    # NOTE: It is at least the user's responsibility to use [link](./filename)
    # NOTE: For now user has to write link paths relative to root directory of zettel
    # NOTE: Relative paths in format
    # NOTE: ./file or ./dir/dir/.../file

    # populate frontlinks
    for markdown in markdowns:
        markdown.update_front_links()

    # populate backlinks now that frontlinks have been updated
    for markdown in markdowns:
        markdown.update_back_links(markdowns)

    # update metadata: type, links, backlinks using yaml
    for markdown in markdowns:
        markdown.update_metadata()

    # using os.path.basename(path)
    # draw_tree(links)

    # loop through links[name] and for each link add the corresponding backlink to file if it exists
    # if file does not exist add link name to a links["to-do"]

    # create draw_tree() function to create a tree based on links and backlinks
