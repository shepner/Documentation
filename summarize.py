#!`which python3`
"""
# summarize.py

## Purpose

The purpose of this application is to scan through all of the documents within the repository and generate a single summary file which can be used to access them
"""

"""
## Structure

``` pseudocode
read contents of repo
  if *.yaml file
    parse YAML
    generate tabular output in html:
      layout: "[title](URL)", "shortDescription", "most recent revision date", "most recent revision status"
      convert MD to html
save file to summary.html
```

## References
* [PyYAML](https://pyyaml.org/)
* [CommonMark/MarkDown](https://github.com/readthedocs/commonmark.py)

"""

# code goes here


