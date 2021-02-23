import GUI
from PubmedCrawler import AbstractLister

#main loop
Sgui = GUI.Search_GUI()

try:
    while True:
        value = Sgui.show()
        abstract_list = AbstractLister(search_terms = value, page_number = 2).getList()
        Sgui.update(abstract_list)
except:
    print('Exited')
