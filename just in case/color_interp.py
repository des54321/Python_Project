def lerp(least,most,index):
    return least + (most - least)*index


class ColorLerp:

    def __init__(self, colors, positions) -> None:
        '''
        A simple class that easily allows for interpolating between colors given an index between 0 - 1
        An example could be one that goes between blue, violet, and then to green
        You would speicify those colors in the colors list: [blue, violet, green], (it would need to be in the form (red,green,blue))
        Then the positions list would just be where violet is, so mabye [0.4]

        colors: What the start, end, and middle colors are, will use the positions to determine where middles colors go
        positions: Where the middle colors are
        '''
        self.colors = colors
        self.postions = tuple([0] + list(positions) + [1])
    
    
    
    def get(self, index):
        if len(self.colors) == 1 or index == 0:
            return self.colors[0]
        elif index == 1:
            return self.colors[-1]
        else:
            between = 0
            for n,i in enumerate(self.postions):
                if index < i:
                    between = n
                    break
            
            lerp_index = (index - self.postions[between-1])/(self.postions[between] - self.postions[between-1])
            return tuple([int(lerp(self.colors[between-1][i],self.colors[between][i],lerp_index)) for i in range(3)])