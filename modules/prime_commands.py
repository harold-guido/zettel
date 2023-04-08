import os
import yaml
import re
from .markdown import Markdown

# declaring variables used throughout module
REGISTERS = ['', '.notes-register', '.references-register', '.projects-register']
FILE_TYPES = ['Note', 'Reference', 'Project']

# HELPER FUNCTIONS
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

def markdown_method(markdowns, method):
    for markdown in markdowns:
        if method == "front":
            markdown.update_front_links()
        elif method == "back":
            markdown.update_back_links(markdowns)
        elif method == "meta":
            markdown.update_metadata()

def has_most_links(markdowns):
    has_most_links = None
    for reference_markdown in markdowns:
        if not isinstance(has_most_links, Markdown):
            has_most_links = reference_markdown
        elif len(reference_markdown.front_links) > len(has_most_links.front_links):
            has_most_links = reference_markdown
    return(has_most_links)

# the tree will have to be one level deep
# divide the functions used to build the tree
def newline_concat(string_list):
    concat_string = ""
    for string in string_list:
        if concat_string == "":
            concat_string = string
        else:
            concat_string += "\n" + string
    return concat_string

# draws one tree per topic
def draw_topic_tree(topic_markdown, markdowns):
    return("Hello World")

# one topic being a node not linked to previously but with the greatest number of links

def draw_tree(markdowns, linked_markdowns=[], previous_markdown=None):
    if len(markdowns.front_links) == 1:
        return(markdowns[0].name)
    else:
        markdown = has_most_links(markdowns)
        markdowns.remove(markdown)
    return("Hello World")
# tree is essentially concatonation of
# "| | | └-file\n"
# ├
# │
# └
# ─
# .append("\n" + draw_tree)

def make_bibliography(markdowns):
    return("Hello World")

# PRIMARY FUNCTIONS
# command: init
def init():
    # initialize zettelkasten in current directory
    current_directory = os.getcwd()
    markdowns = find_markdowns(current_directory)

    # create hidden register
    # use only one register to store all other bibliographies
    os.makedirs(os.path.join(current_directory, ".register"), exist_ok=True)
    # init does not make bibliography files

    print(markdown.name for markdown in markdowns)
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

# command: update
def update(markdowns=[], ):
    if len(markdowns) == 0 : markdowns=find_markdowns(os.getcwd())

    # populate frontlinks
    markdown_method(markdowns, "front")
    # populate backlinks now that frontlinks have been updated
    markdown_method(markdowns, "back")
    # update metadata: type, links, backlinks using yaml
    markdown_method(markdowns, "meta")

    # using os.path.basename(path)
    # draw_tree(markdowns)

    # loop through links[name] and for each link add the corresponding backlink to file if it exists
    # if file does not exist add link name to a links["to-do"]

    # create draw_tree() function to create a tree based on links and backlinks
