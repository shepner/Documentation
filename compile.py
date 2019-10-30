#!`which python3`

"""
experimenting with the idea of using a mix of YAML(ish) and MD for the psodocode/commentary/discussion/etc 
outside of the code's comments to see how it works.  Or perhaps something similar to
the Jupyter Notebook (.IPYNB) file format may also be an option?  Need to explore
"""

"""
read file and parse YAML data
  #pip install pyyaml
"""
import yaml

with open(r'E:\data\categories.yaml') as file:
    documents = yaml.full_load(file)
    for item, doc in documents.items():
        print(item, ":", doc)

"""
structure output file in MD format
"""


"""
output to HTML
  convert [MD](https://github.com/readthedocs/commonmark.py) to html
    #pip install commonmark
  move file to destination
"""
import commonmark

parser = commonmark.Parser()
ast = parser.parse("Hello *World*")
renderer = commonmark.HtmlRenderer()
html = renderer.render(ast)
print(html)


"""
output to PDF
  call [pandoc](https://pandoc.org/) to convert
  move file to destination
"""
