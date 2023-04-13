import PySimpleGUI as sg
from typing import List, Tuple
import colour 


class Track:
    """Represents a track, that is a list of <res> values computed based on the previous track.
    Handles mathematical computations as well as PySimpleGui drawing.
    """
    
    def __init__(self, graph: sg.Graph, base: bool=False) -> None:
        """
        Args:
            graph (sg.Graph): The PySimpleGUI Graph attached to this track
            base (bool, optional): Wether this track is the first one or not. Defaults to False.
        """
        self.graph = graph
        self.base = base    # is this graph the first of the list ?
        self.values = []
        self.res = 4    # default dummy value
    
    def computeElements(self, baseList:List[colour.Color], res:int):
        """Updates <values> based on the given list. 
        A cell will take the color of whichever cell falls at its middle in <baseList>.
        Falling over a border between two cells results ina blank.

        Args:
            baseList (List[colour.Color]): The color list to build this one upon
            res (int): The number of cells in this track
        """
        self.res = res
        
        if self.base :
            # if base, no computations, just recreate a gradient of length <res> 
            self.values = list(colour.Color('red').range_to(colour.Color("purple"), res))
            return
        
        n0 = len(baseList)
        n1 = res
        self.values = [0 for _ in range(n1)]
        
        for k in range(n1):
            clr = colour.Color('white')
            baseIndex = n0 * (k+0.5) / n1   # math formula to compute where the middle of the cell falls
            if not baseIndex.is_integer() : 
                clr = baseList[int(baseIndex)]
            self.values[k] = clr
        
        
    @classmethod
    def BaseTrack(cls, graph: sg.Graph, res:int):
        """Creates a Track object initialized as a base track, i.e. a gradient without blanks.

        Args:
            graph (sg.Graph): The PySImpleGui graph to draw this track on.
            res (int): The number of cells in this track.

        Returns:
            _type_: _description_
        """
        
        t = cls(graph, base=True)
        gradient = list(colour.Color('red').range_to(colour.Color("purple"), res))
        t.values = gradient
        t.res = res
        return t
    
    def updateGraph(self):
        """Updates the PySimpleGui graph of the track base on <values>.
        Often called after using <computeElements>.
        """
        for k, clr in enumerate(self.values):
            self.graph.DrawRectangle((k/self.res, 1), ((k+1)/self.res, 0), fill_color=clr, line_color='black')


def addTrack(window: sg.Window, track: sg.Element):
    """Adds a full track layout (sg.Graph + sg.Slider) to the window

    Args:
        window (sg.Window): The window to add the track on, must have a sg.Column with id "tracks".
        track (sg.Element): The full track layout (sg.Graph and sg.Slider)
    """
    window.extend_layout(window['tracks'], track)
    window['tracks'].contents_changed()

def newTrack(trackIndex: int, winSize: Tuple[int, int], base: bool=False, res: int=None) -> Tuple[Track, List[sg.Element]]:
    """Generates a new track as well as its slider and graph

    Args:
        trackIndex (int): The index of this new track in the layout, i.e. #tracks.
        winSize (Tuple[int, int]): The (width, height) of the window.
        base (bool, optional): Is this new track the first one. Defaults to False.
        res (int, optional): Only call when base=True, the number of cells in the track. Defaults to None.

    Returns:
        Tuple[Track, List[sg.Element]]: The Track object as well as [[graph], [slider]] in their respective list for UI's sake.
    """
    assert not (base and res is None)
    
    graph = sg.Graph((int(winSize[0]*0.8), 50), graph_bottom_left=(0, 0), graph_top_right=(1, 1), float_values=True, background_color="white")
    slider = sg.Slider((1, 100), key=f"slider{trackIndex}", size=(int(winSize[0]*0.3), 10), default_value=4, orientation='h', enable_events=True)
    t = Track.BaseTrack(graph, res) if base else Track(graph)
    return t, [[slider], [t.graph]]


def main():
    size = (800, 400)
    sg.theme('DarkAmber') 
    
    # Initializing
    baseRes = 4
    baseTrack, baseElements = newTrack(0, winSize=size, base=True, res=baseRes)
    tracks = [baseTrack]
    layout = [  
        [sg.Column(baseElements, key='tracks', scrollable=True, vertical_scroll_only=True, expand_y=True)],
        [sg.Button('Nouvelle piste', key='addTrack')]
    ]

    # Creating the Window
    window = sg.Window('Musique déformée', layout, size=size, resizable=True)
    window.Finalize()
    baseTrack.updateGraph()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            break
        
        if event.startswith('slider'):  # if a slider has been moved
            sliderIndex = int(event.replace('slider', ''))  # slider ids : "slider{index}""
            newRes = int(values[event]) # gets the new resolution from the slider
            track = tracks[sliderIndex]
            if sliderIndex > 0: # if not the base track
                track.computeElements(tracks[sliderIndex-1].values, newRes)
            else:
                track.computeElements(None, newRes)
            track.updateGraph()

            for i, t in enumerate(tracks[sliderIndex+1:]):
                # updates every track that comes after to inherit the changes, i.e. recomputing cells
                i += sliderIndex + 1    
                t.computeElements(tracks[i-1].values, t.res)
                t.updateGraph()
        
        elif event == 'addTrack':
            track, elements = newTrack(len(tracks), winSize=size)
            track.computeElements(tracks[-1].values, track.res)
            tracks.append(track)
            
            addTrack(window, elements)
            track.updateGraph()
        
    window.close()


if __name__ == '__main__' : main()