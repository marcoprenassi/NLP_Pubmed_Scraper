import PySimpleGUI as sg

class Search_GUI(object):
    title = "PUBMED SEARCH GUI"
    instructions = []
    instructions.append("->")
    instructions.append("input search terms: ")

    def __init__(self):
        layout = [[sg.Text(self.instructions[0])], [sg.Text(self.instructions[1]), sg.InputText("", key='_SYMPTOMS_LIST_', do_not_clear=False)], [sg.Button("OK")]]
        # Create the window
        self.window = sg.Window(self.title, layout, return_keyboard_events=True)

        # Create an event loop
    def show(self):
        while True:
            event, values = self.window.read()
        # End program if user closes window or
    # presses the OK button
            if event == "OK" or event == sg.WIN_CLOSED or ord(event) == 13:
                print(event,values)
                break

        self.window.close()
        return values.get('_SYMPTOMS_LIST_');

Sgui = Search_GUI();
Sgui.show();
