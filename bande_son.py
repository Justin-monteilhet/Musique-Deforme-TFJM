import PySimpleGUI as sg
import colour

size = (500, 300)

sg.theme('DarkAmber')   

baseGraph = sg.Graph((int(size[0]*0.8), 50), graph_bottom_left=(0, 0), graph_top_right=(1, 1), float_values=True, background_color="white")
editedGraph = sg.Graph((int(size[0]*0.8), 50), graph_bottom_left=(0, 0), graph_top_right=(1, 1), float_values=True, background_color="white")

baseList = []
editedList = []

layout = [  
    [sg.Slider((1, 100), key="slideBase", size=(int(size[0]*0.8), 10), default_value=4, orientation='h', enable_events=True)],
    [baseGraph],
    [editedGraph],
    [sg.Slider((1, 100), key="slideEdited", size=(int(size[0]*0.8), 10), default_value=7, orientation='h', enable_events=True)]
]

# Create the Window
window = sg.Window('Musique déformée', layout, size=size)
window.Finalize()

def make_track(graph, n, l:list):
    clr_list = list(colour.Color('red').range_to(colour.Color("purple"), n))
    l.clear()
    for i in range(n):
        hex = clr_list[i].hex
        l.append(hex)
        baseGraph.DrawRectangle((i/n, 1), ((i+1)/n, 0), fill_color=hex, line_color="black")

def make_edited(graph, l:list):
    res = len(l)
    for i in range(res):
        hex = l[i]
        graph.DrawRectangle((i/res, 1), ((i+1)/res, 0), fill_color=hex, line_color="black")
        
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break
    
    baseRes = int(values['slideBase'])
    make_track(baseGraph, baseRes, baseList)

    
    editedRes = int(values['slideEdited'])
    editedList.clear()
    for i in range(editedRes):
        index = baseRes*(i+0.5)/editedRes
        if index.is_integer() : editedList.append(colour.Color('white'))
        else : editedList.append(baseList[int(index)])
        
    make_edited(editedGraph, editedList)
    
window.close()