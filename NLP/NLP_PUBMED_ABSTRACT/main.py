import GUI
from PubmedCrawler import AbstractLister

#main loop
Sgui = GUI.Search_GUI()
pubmed_core = None
strlist = ''

while True:

        GUI_values = Sgui.show()

        #print(GUI_values[4])
        if GUI_values[4] == "search":
            pubmed_core = AbstractLister(search_terms = GUI_values[0], page_number =int(GUI_values[1]) + 1, GUI_Object = Sgui)
            abstract_list = pubmed_core.getList()
        elif(GUI_values[4] == "load_file"):
            pubmed_core = AbstractLister(filename = "AbstractLog.txt", GUI_Object=Sgui)
            print(pubmed_core.abstract_list_raw)
        elif GUI_values[4] == "sentences_extractor":
            NP_list = pubmed_core.sentencesExtractor(GUI_values[3], GUI_values[2])
            print(NP_list)
            Sgui.update(NP_list[:50])
            try:
                file_log = open("NP_list.txt", "w+", encoding="utf-8")
                for NP_item in NP_list:
                    file_log.write(str(NP_item))
                    file_log.write('\n')
                file_log.close();
            except:
                print("NP_list.txt not writable")


        elif GUI_values[4] == "word_extractor":
            word_list = pubmed_core.wordExtractor()
            Sgui.update(pubmed_core.statistics().most_common(100))
        elif GUI_values[4] == "parameter_extractor":
            chuncked_list = pubmed_core.parameterExtractor()
            Sgui.updateParameterList(chuncked_list)

            i = 0
            j = 0
            k = 0

            total = 0
            ij = 0
            ik = 0
            jk = 0

            for chuncks in chuncked_list:
                combo_1 = False
                combo_2 = False
                combo_3 = False
                if(len(chuncks[2]) != 0):
                    i += 1
                    combo_1 = True
                if(len(chuncks[3]) != 0):
                    j += 1
                    combo_2 = True
                if(len(chuncks[4]) != 0):
                    k += 1
                    combo_3 = True
                if combo_1 and combo_2 and combo_3:
                    total += 1
                elif combo_1 and combo_2:
                    ij += 1
                elif combo_2 and combo_3:
                    jk += 1
                elif combo_1 and combo_3:
                    ik += 1

            print("Articles: " + str(len(chuncked_list)) + "/" + str(len(pubmed_core.abstract_list_raw)) + " Dates: " + str(i) + " Parameters: " + str(j) + " Subjects: " + str(k) + "\nNo Subjects: " + str(ij) +  " No Dates : " + str(jk) +  " No Parameters: " + str(ik) + " All: " + str(total))
