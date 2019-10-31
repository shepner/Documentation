#!`which python3`
"""
# summarize.py

## Purpose

The purpose of this application is to scan through all of the documents within the repository and generate a single summary file which can be used to access them

## Structure

``` pseudocode
read contents of repo
  if *.yaml file
    parse YAML
    generate tabular output in html:
      group by `type`:  1 table per type
      sort by "most recent `revision` `date`" desc
      row layout: "[`title`](URL)", "`shortDescription`", "most recent `revision` `date`", "most recent `revision` `status`"
      convert MD to html
save file to summary.html
```

## References
* [PyYAML](https://pyyaml.org/)
* [CommonMark/MarkDown](https://github.com/readthedocs/commonmark.py)

Scrapers ([StackOverflow - Difference between BeautifulSoup and Scrapy crawler?](https://stackoverflow.com/questions/19687421/difference-between-beautifulsoup-and-scrapy-crawler)
1. parsing library: [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
2. designed for testing: [Selenium](https://www.seleniumhq.org/)
3. web scraper framework: [scrapy](https://scrapy.org/) [docs](https://docs.scrapy.org/en/latest/)

Note: I listed these in the order of preference for this particular use (without too much research into the matter)

## Notes

To assist with this, the GitHub [API](https://developer.github.com/v3/) can [list the repo contents](https://developer.github.com/v3/repos/contents/)

However this would be easier (https://developer.github.com/v3/repos/contents/#get-contents):
https://api.github.com/repos/shepner/Documentation/contents/
Course, it doesnt support recursion so you must look for `"type": "dir",` and do this again

This might be an alternative: https://developer.github.com/v3/git/trees/
get the info about the selected repo: (https://developer.github.com/v3/repos/#get)
https://api.github.com/repos/shepner/Documentation/git/ref/heads/master
extract the sha: "e2c27450bc01609289a44dc0974b787840362575"
and then recursively fetch the into (https://developer.github.com/v3/git/trees/)
https://api.github.com/repos/shepner/Documentation/git/trees/e2c27450bc01609289a44dc0974b787840362575?recursive=1
now fetch the contents of the blobs (https://developer.github.com/v3/git/blobs/#get-a-blob)(https://developer.github.com/v3/media/)
https://api.github.com/repos/shepner/Documentation/git/blobs/73fd97c81cc730973ec704d15474a9d18ee9d083
or perhaps just scrape the path and name and fetch the raw file directly
https://raw.githubusercontent.com/shepner/Documentation/master/1e7c647e-93d7-455d-b5a5-fd7205ca1b14.yaml
"""


#read contents of repo

#initial example code from [here](https://github.com/datasciencedojo/tutorials/blob/master/Web%20Scraping%20with%20Python%20and%20BeautifulSoup/Web%20Scraping%20with%20Python%20and%20Beautiful%20Soup.py)

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client

# URl to web scrap from.
# in this example we web scrap graphics cards from Newegg.com
page_url = "http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=-1&IsNodeId=1&Description=GTX&bop=And&Page=1&PageSize=36&order=BESTMATCH"

# opens the connection and downloads html page from url
uClient = uReq(page_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

# finds each product from the store page
containers = page_soup.findAll("div", {"class": "item-container"})

# name the output file to write to local disk
out_filename = "graphics_cards.csv"
# header of csv file to be written
headers = "brand,product_name,shipping \n"

# opens file, and writes headers
f = open(out_filename, "w")
f.write(headers)

# loops over each product and grabs attributes about
# each product
for container in containers:
    # Finds all link tags "a" from within the first div.
    make_rating_sp = container.div.select("a")

    # Grabs the title from the image title attribute
    # Then does proper casing using .title()
    brand = make_rating_sp[0].img["title"].title()

    # Grabs the text within the second "(a)" tag from within
    # the list of queries.
    product_name = container.div.select("a")[2].text

    # Grabs the product shipping information by searching
    # all lists with the class "price-ship".
    # Then cleans the text of white space with strip()
    # Cleans the strip of "Shipping $" if it exists to just get number
    shipping = container.findAll("li", {"class": "price-ship"})[0].text.strip().replace("$", "").replace(" Shipping", "")

    # prints the dataset to console
    print("brand: " + brand + "\n")
    print("product_name: " + product_name + "\n")
    print("shipping: " + shipping + "\n")

    # writes the dataset to file
    f.write(brand + ", " + product_name.replace(",", "|") + ", " + shipping + "\n")

f.close()  # Close the file

