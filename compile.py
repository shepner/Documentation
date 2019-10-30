#!`which python3`
"""
# summarize.py

## Purpose

The purpose of this application is to publish the YAML formatted document as HTML, PDF, and CommonMark

## Structure

``` pseudocode
read .yaml file
parse YAML
generate document in CommonMark format:
  documentBody
  ---
  # Revision History
  "date", "status", "name", "reason"  <--this is a table
convert CM file to HTML
convert CM file to PDF
write all files to destination
```

## References
* [PyYAML](https://pyyaml.org/)
* [pandoc](https://pandoc.org/)
"""

#pip install pyyaml
import yaml

with open(r'E:\data\categories.yaml') as file:
    documents = yaml.full_load(file)
    for item, doc in documents.items():
        print(item, ":", doc)

