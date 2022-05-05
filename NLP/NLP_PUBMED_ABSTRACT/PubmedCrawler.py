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
    def __init__(self, pmid=None, url='', search_term='', page_number=1):
        page = ''
        if pmid:
            pmid = pmid.strip()
            url = "http://www.ncbi.nlm.nih.gov/pubmed/%s" % pmid
            page = requests.get(url).text
        if search_term:
            for i in range(page_number):
                url = "http://www.ncbi.nlm.nih.gov/pubmed/?term=%s&page=%d" % (
                search_term, i)  # &sort=pubdate to sort on pubblication date
                page += (requests.get(url).text)
        self.soup = BeautifulSoup(page, "html.parser")

    def render(self):
        return self.soup


class AbstractLister(object):
    search_terms = None
    page_number = None
    pubmedObjectCollection = None
    abstract_list = None  ## every Null check
    abstract_list_raw = None
    GUI_Object = None
    abstract_sentences_list_raw = None
    abstract_title_list = None
    full_articles = None

    def __init__(self, GUI_Object, search_terms='', page_number=1, filename=None):
        print(0)
        print(filename)
        self.search_terms = search_terms
        self.page_number = page_number
        self.GUI_Object = GUI_Object
        self.abstract_list = []
        self.abstract_list_raw = []
        self.abstract_sentences_list_raw = []
        self.abstract_title_list = []
        self.full_articles = []

        if filename is None:
            try:
                print(1)
                pubmedObjectCollection = PubMedObject(search_term=self.search_terms,
                                                      page_number=self.page_number).render();
                search_page = pubmedObjectCollection.find_all("span", "docsum-pmid")
                abstract_pmid = []
                [abstract_pmid.append(pmid.text) for pmid in search_page]
                abstract_log_list = ''
                strPmids = ''
                counter = 0;
                # print(abstract_pmid)
                for pmid in abstract_pmid:
                    try:
                        counter += 1;
                        single_article = PubMedObject(pmid=pmid).render()
                        abstract_raw = single_article.find(id='abstract')
                        title = single_article.find("h1", {"class": "heading-title"}, text=True)
                        try:
                            year = 0
                            yearSearch = single_article.find("span", {"class": "citation-year"}, text=True)
                            if yearSearch == None:
                                yearSearch = single_article.find("span", {"class": "cit"}, text=True)
                            print(yearSearch.contents)
                            year = int(yearSearch.contents[0][0:4])
                            print(year)
                        except Exception:
                            print("failed year")
                        self.full_articles.append(single_article)
                        Pmids_and_title_str_temp = pmid + ": " + strPmids.join(str.strip() for str in title.contents)
                        strPmids = strPmids + Pmids_and_title_str_temp + "\n"

                        self.abstract_title_list.append(strPmids)

                        GUI_Object.update(strPmids)
                        self.abstract_list_raw.append((year, Pmids_and_title_str_temp, abstract_raw.text.lower()))
                        abstract_log_list = abstract_log_list + ("\nAbstract\n" + "\n  Year: " + str(
                            year) + "\n  Title: " + Pmids_and_title_str_temp + "\n  Body: " + abstract_raw.text.lower())

                        sentences_temp = nltk.sent_tokenize(abstract_raw.text.lower())
                        sentences_temp = [nltk.word_tokenize(sent) for sent in sentences_temp]
                        self.abstract_sentences_list_raw.append((Pmids_and_title_str_temp, sentences_temp))
                        sentences_temp = [nltk.pos_tag(sent) for sent in sentences_temp]
                        self.abstract_list.append(sentences_temp)
                        print(counter)
                    except Exception as e:
                        print(e)
                try:
                    file_log = open("AbstractLog.txt", "w+", encoding="utf-8")
                    file_log.write(abstract_log_list)
                    file_log.close();
                except Exception as e:
                    print(e)
            except:
                print('Search failed')
        else:
            self.GUI_Object = GUI_Object
            try:
                print(2)
                print(filename)
                fopen = open(filename, "r", encoding="utf-8")
                abstracts_raw = fopen.read()
                loaded_abstracts = re.split('Abstract', abstracts_raw)
                fopen.close()

                for abstract in loaded_abstracts:
                    try:
                        if (len(abstract) > 20):
                            year = re.search("(?<=Year: )\d+", abstract)
                            year = int(year.group())
                            title = re.search("(?<=Title: ).+", abstract)
                            title = title.group()
                            bodyStart = re.search("(?<=Body).+", abstract)
                            body = abstract[bodyStart.end():len(abstract)]

                            self.abstract_list_raw.append((year, title, body))
                            sentences_temp = nltk.sent_tokenize(abstract)
                            sentences_temp = [nltk.word_tokenize(sent) for sent in sentences_temp]
                            self.abstract_sentences_list_raw.append(sentences_temp)
                            sentences_temp = [nltk.pos_tag(sent) for sent in sentences_temp]
                            self.abstract_list.append(sentences_temp)
                    except:
                        print('No text found')
            except Exception:
                print(Exception)

    def getList(self):
        return self.abstract_list

    def sentencesExtractor(self, grammar, node_word):
        cp = nltk.RegexpParser(grammar)
        chuncked_list = [];
        chuncked_data = [];
        NP_list = [];
        for abstract in self.abstract_list:
            for nouns in abstract:
                chuncked_data.append(cp.parse(nouns))
            chuncked_list.append(chuncked_data)
            for chuncks in chuncked_data:
                for node in chuncks:
                    if type(node) == nltk.tree.Tree:
                        words = [w for w, t in node.leaves()]
                        try:
                            if node_word is None:
                                idx = [i for i, item in enumerate(words)]
                            else:
                                idx = [i for i, item in enumerate(words) if re.search(node_word, item)]
                            treeposition = node.leaf_treeposition(idx[0])
                            NP_list.append(node[treeposition[:-1]])
                            # print(treeposition);
                            # print(chuncks[ treeposition[:-1] ])
                            # self.GUI_Object.update(NP_list)
                        except:
                            a = 0
            chuncked_data = []

        return NP_list

    def parameterExtractor(self):
        chuncked_list = [];
        NP_list = [];
        time_list = []
        parameter_list = []
        patients_list = []
        matching_boolean = False
        corpus_time = ['days', 'months', 'years']
        corpus_parameters = ['s', 'ms', 'μs', 'hz', 'khz', 'V', 'A', 'mA', 'μA', 'mV', 'μV', 'channels']
        corpus_patients = ['patients', 'subjects', 'elderly', 'young']

        i = 0
        words = None
        try:
            for abstract in self.abstract_list_raw:

                words = nltk.regexp_tokenize(abstract[2], '(\d*\.?\d+)\s?(\w+)')
                if words != None:
                    for word in words:
                        for time in corpus_time:
                            if word[1] == time:
                                time_list.append(word)
                                print('time: ' + str(word))
                                matching_boolean = True
                        for parameter in corpus_parameters:
                            if word[1] == parameter:
                                parameter_list.append(word)
                                print('parameter: ' + str(word))
                                matching_boolean = True
                        for patient in corpus_patients:
                            if word[1] == patient:
                                patients_list.append(word)
                                print('patient: ' + str(word))
                                matching_boolean = True

                print(words)
                if matching_boolean:
                    chuncked_list.append(
                        (abstract[0], abstract[1], time_list.copy(), parameter_list.copy(), patients_list.copy()))
                    matching_boolean = False
                time_list.clear()
                parameter_list.clear()
                patients_list.clear()
            # [chuncked_list.append(abstract) for abstract in self.abstract_list_raw if re.search("\d*\.?\d+)\s?(\w+)",abstract)]
        except Exception:
            print('failed')
            # chuncked_list.append(chuncked_data)
        chuncked_data = []
        return chuncked_list

    def wordExtractor(self):
        return self.abstract_sentences_list_raw

    def statistics(self):
        stopwords = nltk.corpus.stopwords.words('english')
        punctuation = [',', '.', ';', ':', '(', ')']
        complete_corpus = stopwords + punctuation
        allWords = ''
        for abstract in self.abstract_list_raw:
            allWords += abstract[2]
        word_freq = FreqDist(word for word in word_tokenize(allWords))
        dict_filter = lambda word_freq, complete_corpus: dict(
            (word, word_freq[word]) for word in word_freq if word not in complete_corpus)
        filtered_word_freq = dict_filter(word_freq, complete_corpus)
        return nltk.FreqDist(filtered_word_freq)

# print(AbstractLister(search_terms = 'wrist', page_number = 2).statistics())
# %%
