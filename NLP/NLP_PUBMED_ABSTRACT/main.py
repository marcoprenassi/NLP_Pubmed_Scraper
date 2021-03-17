import GUI
from PubmedCrawler import AbstractLister
import nltk


#main loop
Sgui = GUI.Search_GUI()
pubmed_core = None
strlist = ''
while True:
    values = Sgui.show()
    print(values[4])
    if values[4] == "search":
        pubmed_core = AbstractLister(search_terms = values[0], page_number = int(values[1])+1, GUI_Object = Sgui)
        abstract_list = pubmed_core.getList()
    elif(values[4] == "load_file"):
        pubmed_core = AbstractLister(filename = "AbstractLog.txt", GUI_Object=Sgui)
        print(pubmed_core.abstract_list_raw)
    elif values[4] == "sentences_extractor":
        NP_list = pubmed_core.sentencesExtractor(values[3], values[2])
        print(NP_list)
        Sgui.update(NP_list[:50])
    elif values[4] == "word_extractor":
        word_list = pubmed_core.wordExtractor()
        Sgui.update(pubmed_core.statistics().most_common(100))
    elif values[4] == "parameter_extractor":
        chuncked_list = pubmed_core.parameterExtractor()
        Sgui.update(chuncked_list)
