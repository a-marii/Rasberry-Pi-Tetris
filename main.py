import random
from sense_hat import SenseHat
import time

hat = SenseHat()

# Screen dimensions
WIDTH, HEIGHT = 8, 8
GRID_SIZE = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
COLORS = [RED, BLUE, GREEN]

# Tetromino shapes
SHAPES = [
    [
        ['OOOO',
         '....',
         '....',
         '....'],
        [
         '..O.',
         '..O.',
         '..O.',
         '..O.']
    ],
    [
        ['..O.',
         '.OOO',
         '....',
         '....'],
        ['..O.',
         '.OO.',
         '..O.',
         '....'],
        ['.OOO',
         '..O.',
         '....',
         '....'],
        ['..O.',
         '..OO',
         '..O.',
         '....']
    ],
    [
        [
         '..OO',
         '.OO.',
         '....',
         '....'],
        ['.OO.',
         '..OO',
         '....'
         '....'],
        ['.O..',
         '.OO.',
         '..O.',
         '....'],
        ['..O.',
         '.OO.',
         '.O..',
         '....']
    ],
    [
        ['..O.',
         '..O.',
         '..OO',
         '....'],
        ['...O',
         '.OOO',
         '....',
         '....'],
        ['.OO.',
         '..O.',
         '..O.',
         '....'],
        ['.OOO',
         '.O..',
         '....',
         '....']
    ],
]


class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS) # You can choose different colors for each shape
        self.rotation = 0


class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0  # Add score attribute

    def new_piece(self):
        # Choose a random shape
        shape = random.choice(SHAPES)
        # Return a new Tetromino object
        return Tetromino(self.width // 2, 0, shape)

    def valid_move(self, piece, x, y, rotation):
        """Check if the piece can move to the given position"""
        for i, row in enumerate(piece.shape[(piece.rotation + rotation) % len(piece.shape)]):
            for j, cell in enumerate(row):
                try:
                    if cell == 'O' and (self.grid[piece.y + i + y][piece.x + j + x] != 0):
                        return False
                    
                except IndexError:
                    return False
        return True

    def clear_lines(self):
        """Clear the lines that are full and return the number of cleared lines"""
        lines_cleared = 0
        for i, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(self.width)])
        return lines_cleared

    def lock_piece(self, piece):
        """Lock the piece in place and create a new piece"""
        for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    self.grid[piece.y + i][piece.x + j] = piece.color
        # Clear the lines and update the score
        lines_cleared = self.clear_lines()
        self.score += lines_cleared * 100  # Update the score based on the number of cleared lines
        # Create a new piece
        self.current_piece = self.new_piece()
        # Check if the game is over
        if not self.valid_move(self.current_piece, 0, 0, 0):
            self.game_over = True
        return lines_cleared

    def update(self):
        """Move the tetromino down one cell"""
        if not self.game_over:
            if self.valid_move(self.current_piece, 0, 1, 0):
                self.current_piece.y += 1
            else:
                self.lock_piece(self.current_piece)
    def draw(self):
        """Draw the grid and the current piece"""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                  hat.set_pixel(x,y,cell)

        if self.current_piece:
            for i, row in enumerate(self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        x=self.current_piece.x + j
                        y= self.current_piece.y  + i
                        if(x <=7 and x>=0):
                          hat.set_pixel(x,y,self.current_piece.color)
def draw_game_over(score):
    time.sleep(2)
    while True:
        hat.show_message("Score ")
        hat.show_message(str(score))
    time.sleep(2)

def main():
    # Create a clock object
    clock = time.time()
    # Create a Tetris object
    game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
    fall_time = 0
    fall_speed = 500  # You can adjust this value to change the falling speed, it's in milliseconds
    while True:
        # Fill the screen with black
        for event in hat.stick.get_events():
          if event.action == "pressed" or event.action == "held":
            # Check for the QUIT event
                if event.direction =='left':
                    if game.valid_move(game.current_piece, -1, 0, 0):
                        game.current_piece.x -= 1 # Move the piece to the left
                if event.direction == 'right':
                    if game.valid_move(game.current_piece, 1, 0, 0):
                        game.current_piece.x += 1 # Move the piece to the right
                if event.direction == 'down':
                    if game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1 # Move the piece down
                if event.direction == 'middle':
                    if game.valid_move(game.current_piece, 0, 0, 1):
                        game.current_piece.rotation += 1 # Rotate the piece
              
        # Get the number of milliseconds since the last frame
        delta_time = time.time() 
        # Add the delta time to the fall time
        fall_time += delta_time 
        if fall_time >= fall_speed:
            # Move the piece down
            game.update()
            hat.clear()
            # Reset the fall time
            fall_time = 0
        # Draw the score on the screen
        # Draw the grid and the current piece
        game.draw()
        if game.game_over:
            # Draw the "Game Over" message
            draw_game_over(game.score)  # Draw the "Game Over" message

        # Set the framerate
        time.sleep(1)
        


if __name__ == "__main__":
    main()