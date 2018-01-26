# IS-452-Project

It is a simple scraper to crawl data from indeed.com for the final project of IS452 Foundations of Information Processing at UIUC.

The primary purpose of the project is to build a simple scraper to get the job postings from indeed.com by specifying the keyword and location. To be specific, the main scraper is built with 3 packages respectively: BeautifulSoup, lxml, and Scrapy. The first two are tested in PyCharm whereas the Scrapy is tested in the terminal of Ubuntu since it does not comply with Python 3.6 in Windows OS. Moreover, I attempted to scrape the job descriptions, build the counter for specific job skills and the word cloud based on the job descriptions.

Preparation

1. url_generator

A scraper always needs a start point. After analyzing the patterns used by indeed.com, a URL generator is created to find the start point. The function has several parameters, which are the inputs provided by a user. Having obtained the keyword, city, state, and number of pages to process, the function transforms them into the form that is accessible directly.

2. sub_url_finder

The function is created in order to get all the sub-level/child URLs that can direct to each job description page. They are obviously available as the <href> attribute at the <a> tag under the ‘jobTitle’ class. BeautifulSoup is used here to extract those URLs and they are stored in a list.
  
Main Scrapers

3. BeautifulSoup

Here, I use the request to access the URL of the start page. Notice that the class value for the <div> node differs from ‘row result’, ‘lastRow row result’ and others, with or without extra spaces, I use a regression expression to check the ones containing “row”. There are three fields: title, company, and location. They are touched based on the names of the node and the class values. A loop is applied here to go through all results shown on a specific page and a list of list is used here for organizing the data. A sleep function is added to avoid crashing. Among the three approaches, the BeautifulSoup tends to be the most straightforward one and requires least codes.
  
4. lxml

The process goes similarly to the one with BeautifulSoup. However, the ways to describe what data is needed always differ. Actually, the XPath is used here to specify the locations. An issue solved here is that there are actually two kinds of the path the company name is presented. In one way, it is the text in <a> whose parent node is <span>. In another, it’s parent node is <span> directly. Here, I use a loop to combine those two cases together by mapping the instances. Useless spaces are removed and the results are saved in a list. Among the three approaches, the lxml could be the most structured one and also easy to understand.
  
5. Scrapy

Following the normal structure provided by the documents, I build the sample scraper by defining the items and write the spider files. XPath is used as well, and the issued above is solved correspondingly.

To build a dataset that can be used for other purposes, a .csv file is an output based on the results obtained with the BeautifulSoup. A sample named ‘data analystChampaign.csv’ is the result of: keyword = “data analyst”, city = “Champaign”, state = “IL” and page = 1.

Add-in

Because of the huge variety of the structures of job description page, I attempt to scrape everything by the function desc_scraper() where numbers and punctuations are removed. The strings are split into words and a counter is built. To get better performance, HTML and CSV tags, English stop words and some unrelated words are removed from the counter. Finally, the counter is used to check the frequencies of job skills mentioned in job descriptions and to build a word cloud based on the job descriptions.
