import numpy as np

# class Cell:

#     def __init__(self, value : float = 0.0) -> None:
#         self.value = value
    
#     def set(self, new : float = 0.0) -> None:
#         self.value = new
        


class Grid:

    def __init__(self, width : int, height : int, cell_class : object) -> None:
        self.cell = cell_class
        self.width = width
        self.height = height
        self.data = np.array()
        for i in range(width):
            self.data.append([])
            for x in range(height):
                self.data[-1].append(cell_class())
    
    def replace_cell(self, x : int, y : int, new : object) -> None:
        x %= self.width
        y %= self.height
        self.data[x,y] = new
    
    def get(self, x : int, y : int) -> object:
        x %= self.width
        y %= self.height
        return self.data[x,y]
    
    def is_in(self, x : int, y : int) -> bool:
        if x >= self.width:
            return False
        if x < 0:
            return False
        if y >= self.height:
            return False
        if y < 0:
            return False
        return True