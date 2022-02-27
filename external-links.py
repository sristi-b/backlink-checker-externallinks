import requests
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from slugify import slugify
# slugify("cra#5y ST*&^%ING") will output "cra-5y-st-ing" which is computer friendly.

# List of User Agents: https://developers.whatismybrowser.com/useragents/explore/
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

sitemap_url = "http://papersdrop.com/sitemap.xml"

request = requests.get(sitemap_url, headers=user_agent)
content = request.content
soup = BeautifulSoup(content, 'lxml')

#Get every XML link in the 'Sitemap Homepage'

list_of_locs = soup.find_all("loc")
list_of_xml_links = []

for loc in list_of_locs:
    list_of_xml_links.append(loc.text)
    
#Get a list of published pages URL by diggin into every XML link

print("XML Retrieval Starting")
    
list_of_urls = []

for xml_link in list_of_xml_links:
    
    request = requests.get(xml_link, headers=user_agent)
    content = request.content
    soup = BeautifulSoup(content, 'lxml')

    list_of_locs = soup.find_all("loc")

    for loc in list_of_locs:
        list_of_urls.append(loc.text)
        
print("XML Retrieval complete")
        
#Loop through every URL now and looks for external links:

print("External Links Retrieval Starting")

csv_row_list = []
count = 0
length_list = len(list_of_urls)

for url in list_of_urls:
    
    count = count + 1
    
    request = requests.get(url, headers=user_agent)
    content = request.content
    soup = BeautifulSoup(content, 'lxml')
    
    list_of_links = soup.find_all("a")
    
    list_of_href_values = []

    for link in list_of_links:
        
        try:

            if "papersdrop" in link["href"] or "http" not in link["href"]:

                pass

            else:

                csv_row_list.append([url,link["href"]])
                
        except:
            
            pass
            
    print(count," out of ",length_list," done.")
    
import csv

with open('external_links.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Page URL", "External Link"])
    writer.writerows(csv_row_list)
