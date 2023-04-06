import os
from os.path import relpath
import yaml
import re

class Markdown:
    def __init__(self, path):
        # standard properties
        self.path = path
        self.name = os.path.basename(path)
        self.type_name = ""

        # link collections
        self.front_links = []
        self.back_links = []
        self.broken_links = []

    def update_front_links(self):
        with open(self.path, 'r') as file:
            content = file.read()

        # match the path string inside of each link
        link_pattern = re.compile(r'\[.*?\]\((.*?)\)', re.MULTILINE)

        # match links in file
        # check if links lead to actual files
        for link in link_pattern.findall(content):
            if os.path.isfile(link) and not os.path.samefile(link, self.path):
                # this accounts for self referencing - doesn't allow it
                self.front_links.append(link)
            elif not os.path.samefile(link, self.path):
                # make sure to catch self-referencing from being counted as broken
                self.broken_links.append(link)

        for broken_link in self.broken_links:
            # notify user of broken links
            print(f"Potential broken link: {broken_link} at file: {self.name}")

        # remove duplicates
        for idx_a, reference_link in enumerate(self.front_links):
            for idx_b, check_link in enumerate(self.front_links):
                if os.path.samefile(reference_link, check_link) and idx_a != idx_b:
                    self.front_links.remove(check_link)
        
    def update_back_links(self, other_markdowns):
        for markdown in other_markdowns:
            # first iterates through the other markdowns
            for path in markdown.front_links:
                # then iterates through the front links of the markdown
                if os.path.samefile(path, self.path):
                    # then checks these against the current markdown's own path
                    self.back_links.append(markdown.path)

    def update_metadata(self):
        # uses yaml package to update metadata in the file
        updated_fields = {
            "Type": self.type_name,
            "Front links": ", ".join([os.path.relpath(path) for path in self.front_links]),
            "Back links": ", ".join([os.path.relpath(path) for path in self.back_links])
        }
        metadata_pattern = re.compile(r'^---\n(.*?)\n---', re.DOTALL | re.MULTILINE)

        with open(self.path, 'r') as file:
            content = file.read()

        metadata_match = metadata_pattern.match(content)
        current_metadata = {}

        if metadata_match:
            current_metadata = yaml.safe_load(metadata_match.group(1))
            new_content = content[metadata_match.end()]
        else: 
            new_content = content
        
        current_metadata.update(updated_fields)
        metadata = yaml.dump(current_metadata)

        updated_content = f"---\n{metadata}---\n\n{new_content}"

        with open(self.path, 'w') as file:
            file.write(updated_content)
