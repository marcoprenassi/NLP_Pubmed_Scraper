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
    pubmedObjectCollection = None
    abstract_list = None  ## TODO: every Null check
    abstract_list_raw = None
    GUI_Object = None

    def __init__(self, search_terms, page_number, GUI_Object):
        self.search_terms = search_terms
        self.page_number = page_number
        self.GUI_Object = GUI_Object
        try:
            pubmedObjectCollection = PubMedObject(search_term = self.search_terms, page_number = self.page_number).render();
            search_page = pubmedObjectCollection.find_all("span","docsum-pmid")
            abstract_PMID = []
            [abstract_PMID.append(pmid.text) for pmid in search_page]
            self.abstract_list = []
            self.abstract_list_raw = []
            strPmids = ''
            print(abstract_PMID)
            for pmid in abstract_PMID:
                try:
                    single_article = PubMedObject(pmid = pmid).render()
                    abstract_raw = single_article.find(id='abstract')
                    title = single_article.find("h1", {"class": "heading-title"},text=True)
                    print(pmid+ ": \n")
                    strPmids = strPmids+ pmid+ ": "+  strPmids.join(str.strip() for str in title.contents) + "\n"
                    GUI_Object.update(strPmids)
                    sentences_temp = nltk.sent_tokenize(abstract_raw.text.lower())
                    sentences_temp = [nltk.word_tokenize(sent) for sent in sentences_temp]


                    self.abstract_list_raw.append(sentences_temp)
                    sentences_temp = [nltk.pos_tag(sent) for sent in sentences_temp]
                    self.abstract_list.append(sentences_temp)
                except Exception as e:
                    print(e)
        except:
            print('Search failed')

    def getList(self):
        return self.abstract_list

    def sentencesExtractor(self, grammar, node_word):
        cp = nltk.RegexpParser(grammar)
        chuncked_list = [];
        chuncked_data = [];
        NP_list =  [];
        for abstract in self.abstract_list:
            for nouns in abstract:
                chuncked_data.append(cp.parse(nouns))
            chuncked_list.append(chuncked_data)
            for chuncks in chuncked_data:
                for node in chuncks:
                    if type(node) == nltk.tree.Tree:
                            words = [ w for w, t in node.leaves() ]
                            try:
                                if node_word is None:
                                    idx = [i for i, item in enumerate(words)]
                                else:
                                     idx = [i for i, item in enumerate(words) if re.search(node_word, item)]
                                treeposition = node.leaf_treeposition(idx[0])

                                NP_list.append(node[ treeposition[:-1] ])
                                #print(treeposition);
                                #print(chuncks[ treeposition[:-1] ])
                                print(node[ treeposition[:-1] ])
                            except:
                                a = 0
            chuncked_data = []
        return NP_list

    def wordExtractor(self):
        return self.abstract_list_raw

    def statistics(self):
        stopwords = nltk.corpus.stopwords.words('english')
        punctuation = [',','.',';',':','(',')']
        allWords = []
        for abstracts in self.abstract_list_raw:
            for wordList in abstracts:
                allWords += wordList

        word_freq = nltk.FreqDist(allWords)
        dict_filter = lambda word_freq, stopwords, punctuation: dict( (word,word_freq[word]) for word in word_freq if word not in (stopwords or punctuation))

        filtered_word_freq = dict_filter(word_freq, stopwords, punctuation)

        return nltk.FreqDist(filtered_word_freq)


#print(AbstractLister(search_terms = 'wrist', page_number = 2).statistics())
#%%
