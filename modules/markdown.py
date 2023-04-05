import os
import yaml
import re

class Markdown:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.type_name = ""
