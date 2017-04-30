#!/usr/bin/env python
import os
import sys
import json
import jinja2

with open("output.json") as f:
    content = json.load(f)
    templateLoader = jinja2.FileSystemLoader( searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "template.html"
    template = templateEnv.get_template( TEMPLATE_FILE )
    outputText = template.render(content=content)
    print(outputText)
