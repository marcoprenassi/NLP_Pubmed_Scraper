import PySimpleGUI as sg

class Search_GUI(object):
    title = "PUBMED SEARCH GUI"
    instructions = []
    instructions.append("->")
    instructions.append("input search terms: ")
    window = [];

    def __init__(self):
        layout = [[sg.Text(self.instructions[0])], [sg.Text(self.instructions[1]), sg.InputText(size=(50,1), key='_SYMPTOMS_LIST_', do_not_clear=False)], [sg.Button("OK")],[sg.Multiline(size=(80,30), key = "__OUTPUT_TEXT__")]]
        # Create the window
        self.window = sg.Window(self.title, layout, return_keyboard_events=True)

        # Create an event loop
    def show(self):

        while True:
            event, values = self.window.read()

        # End program if user closes window or
    # presses the OK button
            if event == "OK" or ((len(event) == 1) and (ord(event) == 13)):
                #print(event,values)
                break
        return values.get('_SYMPTOMS_LIST_');

    def update(self,results):
        self.window['__OUTPUT_TEXT__'].update(results);
