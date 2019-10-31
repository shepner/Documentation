#!`which python3`
"""
# publish.py

## Purpose

The purpose of this application is to publish the YAML formatted document as HTML, PDF, and CommonMark

## Structure

``` pseudocode
read .yaml file
parse the YAML contents
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
* [requests](https://requests.kennethreitz.org)
"""

#pip install requests
#pip install pyyaml

URL='https://raw.githubusercontent.com/shepner/Documentation/master/1e7c647e-93d7-455d-b5a5-fd7205ca1b14.yaml'

#read .yaml file
import requests
r = requests.get(URL)
r.status_code
#r.headers['content-type']
#r.encoding
#r.text
#r.json()
r.content

#parse the YAML contents
import yaml

documents = yaml.load(r.content)
  for item, doc in documents.items():
    print(item, ":", doc)

