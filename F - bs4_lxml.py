import requests
import re
from time import sleep
from bs4 import BeautifulSoup
from lxml import html
from collections import Counter
from wordcloud import WordCloud
import csv

# generate search page URLs according to the keyword, location input and the number of pages required
def url_generator (keyword, city, state, pages = 10):
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

# find all the job description URLs on a specific search result page by BeautifulSoup
def sub_url_finder(url):
    sleep(1) # avoid crashing
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html5lib')
    job_link_area = soup.find(id = 'resultsCol')
    jobs = job_link_area.find_all('a',{'data-tn-element':"jobTitle"})
    urls_tag = [tag.get('href') for tag in jobs]
    urls = ['http://www.indeed.com'+ i for i in urls_tag]
    return(urls)

# crawl company name, location and job title by BeautifulSoup
def content_bs4(url):
    sleep(1) # avoid crashing
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html5lib')
    results = soup.find_all('div',{'class':re.compile(r"row(\s\w+)?")})
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

# touch all the content on the job description page
def desc_scraper(url):
    sleep(1) # avoid crashing
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html5lib')
    text = soup.get_text()
    text = re.sub("[^a-zA-Z+]"," ", text)
    text = text.lower()
    return text

# crawl company name, location and job title by lxml
def content_lxml(url):
    sleep(1) # avoid crashing
    page = requests.get(url).text
    tree = html.fromstring(page)
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    title = tree.xpath('//div[contains(@class, "row")]//a[@data-tn-element="jobTitle"]/@title', namespaces = ns)
    location = tree.xpath('//div[contains(@class, "row")]//span[@class="location"]/text()', namespaces = ns)
    # two cases of company name
    company_nota = tree.xpath('//div[contains(@class, "row")]//span[@class="company"]/text()', namespaces = ns)
    company_ina = tree.xpath('//div[contains(@class, "row")]//span[@class="company"]/a/text()', namespaces = ns)
    # combine the two cases above into one by matching the instances
    ka = 0
    for kn in range(len(company_nota)):
        if company_nota[kn] == '\n    ':
            company_nota[kn] = company_ina[ka]
            ka += 1
        kn += 1
    company = []
    for item in company_nota:
        company.append(item.strip('    \n'))
    table = []
    row = []
    for num in range(len(title)):
        row.append(title[num])
        row.append(company[num])
        row.append(location[num])
        table.append(row)
        row = []
    return (table)

# a simple test - search for the data analyst postions in Champaign
test_keyword = input("Please input a keyword to search:")
test_city = input("Please input a city to search:")
test_state = input("Please input a state to search (2-digit):")
test_page = input("Please specify how many pages to search:")
test_input = url_generator(test_keyword,test_city,test_state,eval(test_page))
for link in test_input: # Beautiful Soup
    test_result_b = content_bs4(link)
    urls = sub_url_finder(link)
for link in test_input: # lxml
    test_result_l = content_lxml(link)
print("Result by BeautifulSoup")
print(test_result_b)
print("Result by lxml")
print(test_result_l)

# get job descriptions
job_desc = []
for j in range(len(urls)):
    description = desc_scraper(urls[j])
    job_desc.append(description)

# string to words
words = []
for item in job_desc:
    string = item.split(" ")
    words.append(string)

# build a counter
c = Counter()
for item in words:
    eachcounter = Counter(item)
    c += eachcounter

# a list to remove tags, stopwords, and irrelated ones
remove_list = [
# Html Tags
'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'base', 'bdi', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'cite',
'code', 'col', 'colgroup', 'datalist', 'dd', 'del', 'dfn', 'div', 'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'font', 'footer',
'form', 'frame', 'frameset', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'hr', 'html', 'header', 'iframe', 'img', 'ins', 'kbd', 'label', 'li', 'link'
'main', 'mark', 'menuitem', 'meta', 'meter', 'nav', 'noscript', 'ol', 'optgroup', 'option', 'p', 'param', 'pre', 'q', 'rp', 'rt', 'ruby', 's', 'samp',
'script', 'section', 'select', 'source', 'span', 'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'title', 'tr', 'u'
'ul', 'var', 'video', 'wbr', 'cspan'
# Common Stopwords
'a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can'
'cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him',
'his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither',
'no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than',
'that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where',
'which','while','who','whom','why','will','with','would','yet','you','your',
# CSS and others
'e', 'px', 'a', 'c', 'f', 'color', 'id', 'none', 'border', 'function', 'icl', 'margin', 'o', 'style', 'background', 'size', 'r', 'top', 't', 'dir',
'data', 'd', 'display', 'btn', 'ul', 'bottom', 'return', 'sans', 'box', 'text', 'document', 'padding', 'shadow', 'webkit', 'serif', 'window', '+',
'pt', 'solid', 'navigation', 'class', 'cfont', 'inline', 'co', 'ga','gradient','new', 'left', 'radius', 'follow', 'hover', 'sg', 'active', 'true',
'rem','height','width', 'disabled','moz','block','com','face','jquery','image','linear','arial','apply','mso','m','l','js','push','alert','msnormal',
'location','false','work','helvetica','bold','nbsp','transparent','ff','cdiv','ph','page','n','element','category','job','content','icon','key','gxbc',
'v','icims','gbxc','g','short','https','hedeus','ppc','click','h','default','wgg','ui','w','mh','py','tevent','href','tat','yv','jqg','tei','family',
'linkele','family','phs','type','msonormal','u','reqlistitem','rgba','search','url','tahoma','roman','crankshaft','plant','state','left','right','comment',
'widget','bind','overriden','geturl','cookie','domain','parent','browser','svg','error','xml','list','action','posting','event','yu',
'job','indeed','jobposting','paid+sponsored+posting','job+posting','jobs','email','repeat','employer','indeedapplyemployeremail','stop','pagerdivid',
'div+','+div','acdiv','tk','vjtk','tab','account','unconfirmedaccountfollowingdisplay','gender','orientation','user','sgqpnz','date','viewjobrec',
'aci','st','validateform','updaterequestid','link','jobcartlinktext','veteran','']
for rm in remove_list:
    del c[rm]

# to explore how many times Python is mentioned in job descriptions
test_python = Counter({'Python':c['python']})
print(test_python)

# output as .csv
csv_file_name = test_keyword + test_city + ".csv"
outfile = open(csv_file_name, 'w', newline='')
csv_out = csv.writer(outfile)
csv_out.writerow( ['title', 'company', 'location'] )
csv_out.writerows(test_result_b)
outfile.close()

# build a sample word cloud
c_list = list(c)
c_str = ' '.join(list(c))
wc_test = WordCloud().generate(c_str)
import matplotlib.pyplot as plt
plt.imshow(wc_test)
plt.axis('off')
plt.show()
