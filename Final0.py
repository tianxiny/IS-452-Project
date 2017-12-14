from bs4 import BeautifulSoup
from time import sleep
import requests
import re
from collections import Counter
from wordcloud import WordCloud


def url_generator (keyword, city, state, pages = 10): # to generate search page URLs according to the keyword, location input and the number of pages required
    # modify inputs
    keyword = keyword.strip().replace(' ','+')
    city = city.strip().replace(' ','+')
    state = state.strip()

    # build a list to store all links
    url_list = []
    base_url = 'https://www.indeed.com/jobs?q='+keyword+'&l='+city+'%2C+'+state+'&start='
    for page_num in range(pages):
        url = base_url + str(page_num*10)
        url_list.append(url)
    return url_list

def sub_url_finder(url): # find all the job description URLs on a specific search page
    sleep(1) # avoid crashing
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html5lib')

    job_link_area = soup.find(id = 'resultsCol')
    jobs = job_link_area.find_all('a',{'data-tn-element':"jobTitle"})
    urls_tag = [tag.get('href') for tag in jobs]
    urls = ['http://www.indeed.com'+ i for i in urls_tag]

    return(urls)

def content_parser(url): # to crawl company name, location and job title
    sleep(1) # avoid crashing
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html5lib')

    results = soup.find_all('div',{'class':re.compile(r"row(\s\w+)?")}) # not sure about the regex

    table = []
    j = 0
    for result in results:
        row = []
        company = result.find('span', {'class':'company'}).text.strip()
        location = result.find('span', {'class':'location'}).text.strip()
        title = result. find('a', {'data-tn-element':'jobTitle'}).text.strip()
        row.append(title)
        row.append(company)
        row.append(location)
        table.append(row)
        j += 1

    return(table)

def desc_scraper(url): # touch all the content on the job description page
    sleep(1) # avoid crashing
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html5lib')
    text = soup.get_text()
    text = re.sub("[^a-zA-Z+]"," ", text)
    text = text.lower()
    return text

# a simple test - search for the data analyst postions in Champaign
test_input = url_generator('data analyst','Champaign','IL',1)
for link in test_input:
    test_result = content_parser(link)
    urls = sub_url_finder(link)

print(test_result)
job_desc = []
for j in range(len(urls)):
    description = desc_scraper(urls[j])
    job_desc.append(description)
print(len(job_desc))
print(job_desc)

words = []
for item in job_desc:
    string = item.split(" ")
    words.append(string)

c = Counter()
for item in words:
    eachcounter = Counter(item)
    c += eachcounter
# to explore how many times Python is mentioned in job descriptions
test_python = Counter({'Python':c['python']})

print(test_python)

import csv
outfile = open('indeed-test.csv', 'w', newline='')
csv_out = csv.writer(outfile)
csv_out.writerow( ['title', 'company', 'location'] )
csv_out.writerows(test_result)
outfile.close()

job_desc_str = ''.join(job_desc)
print(type(job_desc_str))
wc_test = WordCloud().generate(job_desc_str)
import matplotlib.pyplot as plt
plt.imshow(wc_test)
plt.axis('off')
plt.show()
