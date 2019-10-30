#!`which python3`

#read file and parse YAML data
#pip install pyyaml
import yaml

with open(r'E:\data\categories.yaml') as file:
    documents = yaml.full_load(file)
    for item, doc in documents.items():
        print(item, ":", doc)

###########

#convert [MD](https://github.com/readthedocs/commonmark.py) to html
#pip install commonmark
import commonmark

parser = commonmark.Parser()
ast = parser.parse("Hello *World*")
renderer = commonmark.HtmlRenderer()
html = renderer.render(ast)
print(html)

#output file to destination site

###########

#call [pandoc](https://pandoc.org/) to convert



