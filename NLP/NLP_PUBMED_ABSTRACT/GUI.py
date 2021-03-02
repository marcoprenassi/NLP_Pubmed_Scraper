import PySimpleGUI as sg

class Search_GUI(object):
    title = "PUBMED SEARCH GUI"
    instructions = []
    instructions.append("Search terms: \t")
    instructions.append("Node word: \t")
    window = [];

    def __init__(self):
        layout = [[sg.Text(self.instructions[0]), sg.InputText(size=(50,1), key='_SEARCH_TERMS_', do_not_clear=False)],
        [sg.Text(self.instructions[1]), sg.InputText(size=(50,1), key='_NODE_WORD_', do_not_clear=False)],
        [sg.Button("Search Pubmed", key="search")],[sg.Button("Work with local abstracts", key="local")],[sg.Multiline(size=(80,30), key = "__OUTPUT_TEXT__")]]
        # Create the window
        self.window = sg.Window(self.title, layout, return_keyboard_events=True)

        # Create an event loop
    def show(self):

        while True:
            event, values = self.window.read()

        # End program if user closes window or
    # presses the OK button
            if event == "search" or event == "local" or ((len(event) == 1) and (ord(event) == 13)):
                #print(event,values)
                break
        return [values.get('_SEARCH_TERMS_'), values.get('_NODE_WORD_'), str(event)];

    def updateListString(self,results):
        stringResults = ''.join(str(res) + "\n" for res in results)
        self.window['__OUTPUT_TEXT__'].update(stringResults);

    def update(self,results):
        self.window['__OUTPUT_TEXT__'].update(results);
        self.window.refresh()
