import nltk, re
import requests
from nltk.probability import FreqDist
from bs4 import BeautifulSoup
from nltk import word_tokenize


# %%
class PubMedObject(object):
    soup = None
    url = None

    # pmid is a PubMed ID
    # url is the url of the PubMed web page
    # search_term is the string used in the search box on the PubMed website
    def __init__(self, pmid=None, url='', search_term='Cortical stimulation', page_number=3):
        page = ''
        if pmid:
            pmid = pmid.strip()
            url = "http://www.ncbi.nlm.nih.gov/pubmed/%s" % pmid
            page = requests.get(url).text
        if search_term:
            for i in range(page_number):
                url = "http://www.ncbi.nlm.nih.gov/pubmed/?term=%s&page=%d" % (search_term, i)
                # &sort=pubdate to sort on pubblication date
                page += (requests.get(url).text)
        self.soup = BeautifulSoup(page, "html.parser")

    def render(self):
        return self.soup


pubmedObjectCollection = PubMedObject(search_term='Cortical Stimulation', page_number=3).render();
print(pubmedObjectCollection.text)
exit()
