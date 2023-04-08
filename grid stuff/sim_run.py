from grid_class import Grid

class Cell:

    def __init__(self, value : float = 0.0) -> None:
        self.value = value
    
    def set(self, new : float = 0.0) -> None:
        self.value = new

def sim(rule : list,width : int,height : int,inputs : list,outputs : list,length : int, output_type : int = 0):

    '''
    rule : is the rule it will use to evaluate the grid, [bias , (x-offset, y-offset, weight), (x-offset, y-offset, weight), ...]
    width : the width of the grid you want to evaluate
    height : the height of the grid you want to evaluate
    inputs : the inputs to the grid, [(x-pos, y-pos, value), (x-pos, y-pos, value), ...]
    ouputs : the outputs to the function, [(x-pos, y-pos), (x-pos, y-pos), ...]
    length : how many times it will iterate
    '''

    grid = Grid(width,height,Cell)
    for n in range(length):
        for i in inputs:
            grid.get(i[0],i[1]).set(i[2])
        grid = interate(grid, rule)
    if output_type == 0:
        final = []
        for i in outputs:
            final.append(grid.get(i[0],i[1]).value)
        return final
    elif output_type == 1:
        return grid

def interate(grid : object, rule : list, output_type : int = 0, max_val : float = 100):

    '''
    rule : is the rule it will use to evaluate the grid, [bias , (x-offset, y-offset, weight), (x-offset, y-offset, weight), ...]
    '''



    new_grid = Grid(grid.width,grid.height,Cell)
    for x in range(new_grid.width):
        for y in range(new_grid.height):
            new_grid.get(x,y).value = grid.get(x,y).value
    for x in range(new_grid.width):
        for y in range(new_grid.height):
            total = 0
            total_used = 0
            for i in rule[1:]:
                # if grid.is_in(x + i[0], y + i[1]):
                total_used += 1
                total += (grid.get(x + i[0], y + i[1]).value) * i[2]
            new_grid.get(x,y).value = (total / total_used) + rule[0]
    for x in range(new_grid.width):
        for y in range(new_grid.height):
            grid.get(x,y).value = max(min(new_grid.get(x,y).value, max_val), -max_val)
    return grid