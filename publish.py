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
  * [TeX Live](https://www.tug.org/texlive/) which is needed to [create a PDF](https://pandoc.org/MANUAL.html#creating-a-pdf)
* [requests](https://requests.kennethreitz.org)

"""

#pip3 install requests
#pip3 install pyyaml
#sudo apt install pandoc
#sudo apt install texlive-latex-recommended

URL='https://raw.githubusercontent.com/shepner/Documentation/master/c54c285f-eeb4-4a42-815f-9ea0656265e2.yaml'

#read .yaml file
import requests

r = requests.get(URL)
#r.status_code
#r.headers['content-type']
#r.encoding
#r.text
#r.json()
#r.content  #this is the body of the page

#parse the YAML contents
import yaml

content = yaml.load(r.content, Loader=yaml.FullLoader)
#content  #this is a python set{} with lists[] and sets{} nested inside

#example of walking the top level set
#for item, value in content.items():
#    print(item, ":", value)

#Structure the page and write it to a file
f = open(content['id']+'.md', 'w')  #open a file for output

print ("<title>",content['title'],"</title>", file=f)

print ("\n---\n", file=f)

print (content['documentBody'], file=f)

print ("\n---\n", file=f)

#print the revisions as a table in HTML because it isnt supported by CommonMark
print ("<table>", file=f)
print ("  <tr>", file=f)
print ("    <th>Date</th>", file=f)
print ("    <th>Name</th>", file=f)
print ("    <th>Reason</th>", file=f)
print ("  </tr>", file=f)
#the 'revisions' key consists of a list of sets
#`content['revision'][0]['date']` will provide that specific data element
for element in content['revision']:  #step through the list elements
    print ("  <tr>", file=f)
    #now print the fields
    print ("    <td>",element['date'],"</td>", file=f)
    print ("    <td>",element['name'],"</td>", file=f)
    print ("    <td>",element['reason'],"</td>", file=f)
    print ("  </tr>", file=f)
print ("</table>", file=f)

f.close()  #close the file

#convert the CommonMark file into other formats
import subprocess
subprocess.run(['pandoc', content['id']+'.md', "-o", content['id']+'.html'])
#subprocess.run(['pandoc', content['id']+'.md', "-o", content['id']+'.pdf']) #this is generating errors
