# Game if Life simulator, I plan to use this for generating music 
# Jared Smith

class Game(object):
    
    def __init__(self, state, infinite_board = True):
        
        self.state = state
        self.width = state.width
        self.height = state.height
        self.infinite_board = infinite_board
    
    def step(self, count = 1):
        
        for generation in range(count):
            
            new_board = [[False] * self.width for row in range(self.height)]
            
            for y, row in enumerate(self.state.board):
                for x, cell in enumerate(row):
                    neighbours = self.neighbours(x, y)
                    previous_state = self.state.board[y][x]
                    should_live = neighbours == 3 or (neighbours == 2 and previous_state == True)
                    new_board[y][x] = should_live
    
        self.state.board = new_board

    def neighbours(self, x, y):
        
        count = 0
            
        for hor in [-1, 0, 1]:
            for ver in [-1, 0, 1]:
                if not hor == ver == 0 and (self.infinite_board == True or (0 <= x + hor < self.width and 0 <= y + ver < self.height)):
                    count += self.state.board[(y + ver) % self.height][(x + hor) % self.width]
        
        return count

    def display(self):
        return self.state.display()

class State(object):
    
    def __init__(self, positions, x, y, width, height):
        
        active_cells = []
        
        for y, row in enumerate(positions.splitlines()):
            for x, cell in enumerate(row.strip()):
                if cell == 'o':
                    active_cells.append((x,y))
        
        board = [[False] * width for row in range(height)]
        
        for cell in active_cells:
            board[cell[1] + y][cell[0] + x] = True
                
        self.board = board
        self.width = width
        self.height = height

    def display(self):
        
        output = ''
            
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if self.board[y][x]:
                    output += ' o'
                else:
                    output += ' .'
            output += '\n'
        
        return output

# Tried with a glider
glider = """ oo.
    o.o
    o.. """

my_game = Game(State(glider, x = 2, y = 3, width = 10, height = 10))
i  = 2
while True:
    print my_game.display()
    my_game.step(i)
    i += 1