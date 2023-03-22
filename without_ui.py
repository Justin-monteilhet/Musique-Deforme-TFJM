from typing import List
import colour


def simplify_list(l:list):
    l = list(map(str, l))
    vals = list(set(l))
    d = {}
    for i, val in enumerate(vals):
        d[val] = i
    
    
    return [d[val] for val in l]


class Track:
    """Represents a track, that is a list of <res> values computed based on the previous track.
    Handles mathematical computations as well as PySimpleGui drawing.
    """
    
    def __init__(self, base: bool=False) -> None:
        """
        Args:
            graph (sg.Graph): The PySimpleGUI Graph attached to this track
            base (bool, optional): Wether this track is the first one or not. Defaults to False.
        """
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
    def BaseTrack(cls, res:int):
        """Creates a Track object initialized as a base track, i.e. a gradient without blanks.

        Args:
            graph (sg.Graph): The PySImpleGui graph to draw this track on.
            res (int): The number of cells in this track.

        Returns:
            _type_: _description_
        """
        
        t = cls(base=True)
        gradient = list(colour.Color('red').range_to(colour.Color("purple"), res))
        t.values = gradient
        t.res = res
        return t
    

if __name__ == '__main__':

    baseRes = 23
    t = Track.BaseTrack(baseRes)
    tracks = [t]

    # for res in [9, 7]:
    #     t = Track()
    #     t.computeElements(tracks[-1].values, res)
    #     tracks.append(t)

    for res in range(baseRes+4, 100, 4):
        t = Track()
        t.computeElements(tracks[-1].values, res)
        tracks.append(t)

    final = Track()
    final.computeElements(tracks[-1].values, baseRes)
    print(simplify_list(final.values))

    print("")   