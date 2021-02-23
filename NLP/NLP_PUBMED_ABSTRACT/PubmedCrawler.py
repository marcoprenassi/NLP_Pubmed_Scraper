import sys
import nltk, re, pprint
import requests
from nltk.probability import ConditionalFreqDist
from nltk.probability import FreqDist
from nltk import tokenize
#%%
from bs4 import BeautifulSoup
#%%
from nltk import word_tokenize
#%%
class PubMedObject(object):
    soup = None
    url = None
    # pmid is a PubMed ID
    # url is the url of the PubMed web page
    # search_term is the string used in the search box on the PubMed website
    def __init__(self, pmid=None, url='', search_term='', page_number=1):
        page = ''
        if pmid:
            pmid = pmid.strip()
            url = "http://www.ncbi.nlm.nih.gov/pubmed/%s" % pmid
            page = requests.get(url).text
        if search_term:
            for i in range(page_number):
                url = "http://www.ncbi.nlm.nih.gov/pubmed/?term=%s&page=%d" % (search_term,i)
                page += (requests.get(url).text)
        self.soup = BeautifulSoup(page, "html.parser")

    def render(self):
        return self.soup

class AbstractLister(object):
    search_terms = None
    page_number = None

    def __init__(self, search_terms, page_number):
        self.search_terms = search_terms
        self.page_number = page_number

    def getList(self):
        try:
            pubmedObject = PubMedObject(search_term = self.search_terms, page_number = self.page_number).render();
            search_page = pubmedObject.find_all("span","docsum-pmid")
            abstract_PMID = []
            [abstract_PMID.append(pmid.text) for pmid in search_page]
            abstract_list = []
            print(abstract_PMID)
            for pmid in abstract_PMID:
                single_article = PubMedObject(pmid = pmid).render()
                abstract_raw = single_article.find(id='abstract')
                print(pmid)
                sentences_temp = nltk.sent_tokenize(abstract_raw.text.lower())
                sentences_temp = [nltk.word_tokenize(sent) for sent in sentences_temp]
                sentences_temp = [nltk.pos_tag(sent) for sent in sentences_temp]
                print(sentences_temp)
                abstract_list.append(sentences_temp)
        except:
            print('No readable article')

        return abstract_list


#%%
