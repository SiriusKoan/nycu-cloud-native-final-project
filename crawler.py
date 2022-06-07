import requests
from time import sleep
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from flask import Flask, send_file
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class GoogleCrawler():
    def __init__(self):
        self.url = 'https://www.google.com/search?q='    

    def get_source(self,url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(e)

    # URL萃取器，有link之外，也有標題
    #     qdr:h (past hour)
    #     qdr:d (past day)
    #     qdr:w (past week)
    #     qdr:m (past month)
    #     qdr:y (past year)
    def google_search(self,query,timeline='',page='0'):
        url = self.url + query + '&tbs={timeline}&lr=lang_en'.format(timeline=timeline)
        #url = self.url + query + '&tbs={timeline}&start={page}&lr=lang_en&tbm=nws'.format(timeline=timeline,page=page)
        print('[Check][URL] URL : {url}'.format(url=url))
        response = self.get_source(url)
        return self.parse_googleResults(response)

    # Google Search Result Parsing
    def parse_googleResults(self,response):

        css_identifier_result = "tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = "yuRUbf"
        css_identifier_text = "VwiC3b"
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.findAll("div", {"class": css_identifier_result})
        output = []
        for result in results:
            item = {
                'title': result.find(css_identifier_title).get_text(),
                'link': result.find("div", {"class": css_identifier_link}).find(href=True)['href'],
                'text': result.find("div", {"class": css_identifier_text}).get_text()
            }
            output.append(item)
        return output
    
    def html_parser(self,htmlText):
        soup = BeautifulSoup(htmlText, 'html.parser')
        return soup

    def html_getText(self,soup):
        orignal_text = ''
        for el in soup.find_all('p'):
            orignal_text += ''.join(el.find_all(text=True))
        return orignal_text
    
    def word_count(self, text):
        counts = dict()
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        #words = text.replace(',','').split()
        #print(words)
        for word in words:
            if word not in stop_words:
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
        return counts

    def get_wordcount_json(self,whitelist , dict_data):
        data_array = []
        for i in whitelist:
            json_data = {
                'Date' : 'Week1',
                'Company' : i , 
                'Count' : dict_data.get(i, 0)
            }
            data_array.append(json_data)
        return data_array

    def jsonarray_toexcel(self,data_array):
        df = pd.DataFrame(data=data_array)
        df.to_excel('result.xlsx' , index=False)
        return

app = Flask(__name__)

@app.route("/run")
def crawler_endpoint():
    try:
        nltk.download('popular')
        #query = "TSMC ASML"
        #query = "TSMC SUMCO ASML Applied Materials"
        queries = ["TSMC", "SUMCO", "ASML", "Applied Materials"]
        final_result = []
        for query in queries:
            crawler = GoogleCrawler()
            results = crawler.google_search(query , 'qdr:m')
            for res in results:
                print(res['title'])
                Target_URL = res['link']
                response = crawler.get_source(Target_URL)
                soup = crawler.html_parser(response.text)
                orignal_text = crawler.html_getText(soup)
                #print(orignal_text)
                result_wordcount = crawler.word_count(orignal_text)
                whitelist = ['TSMC', 'SUMCO', 'ASML', 'Applied Materials']
                result = crawler.get_wordcount_json(whitelist, result_wordcount)
                print(result)
                if final_result:
                    for i in range(4):
                        final_result[i]['Count'] += result[i]['Count']
                else:
                    final_result = result
        print(final_result)
        crawler.jsonarray_toexcel(final_result)
        print('Excel is OK')
        return send_file("/crawler/result.xlsx")
    except Exception as e:
        return str(e)

@app.route("/test")
def test_page():
    return "OK"

app.run(host="0.0.0.0")
