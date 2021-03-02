import GUI
from PubmedCrawler import AbstractLister
import nltk


#main loop
Sgui = GUI.Search_GUI()
pubmed_core = None
strlist = ''
while True:
    values = Sgui.show()
    if pubmed_core is None or values[2] == "search":
        pubmed_core = AbstractLister(search_terms = values[0], page_number = 2, GUI_Object = Sgui)
    abstract_list = pubmed_core.getList()
    NP_list = pubmed_core.sentencesExtractor("NP: {<DT|PP\$>?<JJ>*<NN+>}", values[1])
    word_list = pubmed_core.wordExtractor()


    Sgui.update(pubmed_core.statistics().most_common(50))
