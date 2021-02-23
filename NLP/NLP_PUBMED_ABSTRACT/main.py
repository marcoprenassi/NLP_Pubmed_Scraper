import GUI

#main loop
Sgui = GUI.Search_GUI()
value = Sgui.show()

while True:
    try:
        value = Sgui.showResults(value)
    except:
        break
