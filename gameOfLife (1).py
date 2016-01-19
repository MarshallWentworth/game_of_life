import pygame, sys, random
# import tests as T

### Global Variables
WINDOW_SIZE_WIDTH = 1000
WINDOW_SIZE_HEIGHT = 830
WIDTH = 8  # this is the width of an individual square
HEIGHT = 8 # this is the height of an individual square
ALIVE = True
DEAD = False

# RGB Color definitions
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)

check_these_squares = {}
new_squares_to_check = {}

def get_row_top_loc(rowNum, height = HEIGHT):
    """
    Returns the location of the top pixel in a square in
    row rowNum, given the row height.
    """
    return 10 + height * rowNum

def get_col_left_loc(colNum, width = WIDTH):
    """
    Returns the location of the leftmost pixel in a square in
    column colNum, given the column width.
    """
    return 10 + width * colNum

def update_text(screen, message, columns, rows):
    """
    Used to display the text on the right-hand part of the screen.
    """
    textSize = 20
    font = pygame.font.Font(None, 20)
    textY = 0 + textSize
    text = font.render(message, True, white, black)
    textRect = text.get_rect()
    textRect.centerx = (columns + 13) * WIDTH + 10
    textRect.centery = rows
    screen.blit(text, textRect)

def resize_bar(screen, column, row):
    """
    Used to change size and amount of blocks in the screen
    """
    bar = pygame.draw.rect(screen, black, (650, 815, 150, 10))
    circle = pygame.draw.circle(screen, grey, (column, row), 5)
    # bar.centery = rows
    # bar.centerx = columns
    # # screen.blit(bar)

def new_game(size = 10):
    """
    Sets up all necessary components to start a new Game
    of Life.
    """

    total_columns = 100 #int(raw_input("How many columns would you like in your game?\n"))
    total_rows = 100 #int(raw_input("How many rows would you like in your game?\n"))

    pygame.init() # initialize all imported pygame modules

    # window_size = [total_columns * WIDTH + 200, total_rows * HEIGHT + 20] # width, height
    window_size = [WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT]
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Game of Life") # caption sets title of Window 
    
    board = Board(total_columns, total_rows)

    moveCount = 0

    clock = pygame.time.Clock()

    main_loop(screen, board, moveCount, clock, False, True)

def draw_grid(screen, columns, rows):
    """
    Draw the border grid on the screen.
    """

    pygame.draw.line(screen, green, (0 , 0) , (0 , rows * HEIGHT + 20), 20 )
    pygame.draw.line(screen, green, (0 , 0) , (columns * WIDTH + 20 , 0), 20 )
    pygame.draw.line(screen, green, (0 , rows * HEIGHT + 19)  , (columns * WIDTH + 20, rows * HEIGHT + 19) , 20 )
    pygame.draw.line(screen, green, (columns * WIDTH + 19, 0) , (columns * WIDTH + 19, rows * HEIGHT + 30) , 20 )
    for i in range(WIDTH + 10, WIDTH * columns + 10, WIDTH):
        pygame.draw.line(screen, green, (i , 0) , (i , rows * HEIGHT + 20) )
    for i in range(HEIGHT + 10, HEIGHT * rows + 10, HEIGHT):
        pygame.draw.line(screen, green, (0 , i) , (columns * WIDTH + 20 , i) )

# Main program Loop: (called by new_game)
def main_loop(screen, board, moveCount, clock, stop, pause):
    board.squares.draw(screen) # draw Sprites (Squares)
    draw_grid(screen, board.cols, board.rows)
    pygame.display.flip() # update screen
    if stop == True:
        again = raw_input("Would you like to run the simulation again? If yes, type 'yes'\n")
        if again == 'yes':
            new_game()
    while stop == False:     
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #user clicks close
                stop = True
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
            	x_pos, y_pos = pygame.mouse.get_pos()
                print x_pos, y_pos
                if x_pos > 9 and y_pos > 9 and x_pos < 810 and y_pos < 810:
            	    column = (x_pos - 10) / WIDTH
            	    row = (y_pos - 10) / HEIGHT
            	    sqr =  board.get_square(column, row).flip_color()
                    if sqr.is_alive_or_dead:
                        check_these_squares[(column, row)] = sqr
            	# print x_pos, y_pos, board.get_square(column, row).color
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_s:
                    if pause:
                        pause = False
                    else:
                        pause = True
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                	stop = True
                	new_game()


        if stop == False and pause == True: 
            board.squares.draw(screen) # draw Sprites (Squares)
            # ** TODO: draw the grid ** 
            draw_grid(screen, board.cols, board.rows)
            update_text(screen, "Move #" + str(moveCount), board.cols, 20)
            update_text(screen, "Press s to start or pause", board.cols, 35)
            update_text(screen, "Press q to stop and reset", board.cols, 50)
            resize_bar(screen, 700, 800)
            pygame.display.flip() # update screen
            # clock.tick(44)

            #--- Do next move ---#
        elif stop == False and pause == False: 
            board.squares.draw(screen) # draw Sprites (Squares)
            # ** TODO: draw the grid ** 
            draw_grid(screen, board.cols, board.rows)
            update_text(screen, "Move #" + str(moveCount), board.cols, 20)
            update_text(screen, "Press s to start or pause", board.cols, 35)
            update_text(screen, "Press q to stop and reset", board.cols, 50)
            pygame.display.flip() # update screen
            clock.tick(44)

            # Step 1: Rotate class Ant(pygame.sprite.Sprite):
            # ** TODO: rotate the ant and save it's current square ** check!
            # current_square = board.rotate_ant_get_square()
            # board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            # ** TODO: draw the grid here ** check!
            # draw_grid(screen, board.cols, board.rows)
            
            # pygame.display.flip() # update screen
            # clock.tick(44)

            # Step 1:
            # Check if squares should die, live, or be revived.
            for squares in check_these_squares:
                col, row = squares
                board.trial_for_square_or_revival(col, row)
            #     # del check_these_squares[squares]
            # for squares in new_squares_to_check:
            #     check_these_squares[squares] = new_squares_to_check[squares]
                # del new_squares_to_check[squares]

            # Step 2: Flip color of square:
            # ** TODO: flip the color of the square here ** check?

            #current_square = board.get_square()
            # current_square.flip_color()
            board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            # ** TODO: draw the grid here ** check!
            draw_grid(screen, board.cols, board.rows)
            
            pygame.display.flip() #update screen
            clock.tick(44)
            
            # Step 3: Move Ant
            # ** TODO: make the ant step forward here ** check?
            # board.ant.step_forward(board)
            # board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            # ** TODO: draw the grid here ** check!
            # draw_grid(screen, board.cols, board.rows)
            
            # pygame.display.flip() # update screen
            # clock.tick(44)

            # updates check_these_squares and resets new_squares_to_check
            check_these_squares.clear()
            for squares in new_squares_to_check:
                check_these_squares[squares] = new_squares_to_check[squares]

            
            moveCount += 1
            # ------------------------

    pygame.quit() # closes things, keeps idle from freezing

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.rect = self.image.get_rect() # gets a rect object with width and height specified above
                                            # a rect is a pygame object for handling rectangles
        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)
        self.color = color   
        self.image.fill(color)

    def get_rect_from_square(self):
        """
        Returns the rect object that belongs to this Square
        """

        return self.rect

    def flip_color(self):
        """
        Flips the color of the square (white -> black or 
        black -> white)
        """

        if self.color == black:
            self.color = white
        else:
            self.color = black
        self.image.fill(self.color)
        return self

    def is_alive_or_dead(self):
        if self.color == black:
            return ALIVE
        else:
            return DEAD

class Board:
    def __init__(self, columns, rows):

        self.rows = rows
        self.cols = columns
        
        #---Initializes Squares (the "Board")---#
        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = {}
        
        #---Populate boardSquares with Squares---#
        for square_y in range(self.rows):
            for square_x in range(self.cols):
                s = Square(square_y, square_x, white)
                self.boardSquares[(square_x,square_y)] = s
                self.squares.add(s)
    def get_square(self, col, row):
        """
        Given an (x, y) pair, return the Square at that location. Column then Row
        """
        print col,row
        return self.boardSquares[(col, row)]

# class Life:
#     def __init__(self, board, column, row):
#         self.col = column
#         self.row = row
#         self.board = board
   

    def make_square_die(self, col, row): 
        '''
        square dies if it is surrounded with less than 2 alive squares
        or more than 3 alive squares
        '''
        if self.get_square(col, row).is_alive_or_dead():
            self.get_square(col, row).flip_color()

    def revive_square(self, col, row): 
        '''
        square comes back to life if it is surrounded by 3 alive squares
        '''
        if self.get_square(col, row).is_alive_or_dead == False:
            self.get_square(col, row).flip_color()

    def trial_for_square_or_revival(self, col, row):
        
        if self.get_square(col, row).is_alive_or_dead() and self.surrounding_square_counter(col, row) > 3 or self.surrounding_square_counter(col, row) < 2:
            self.make_square_die(col, row)
        if self.get_square(col, row).is_alive_or_dead() == False and self.surrounding_square_counter(col, row) == 3:
            self.revive_square(col, row)

    def surrounding_square_list_maker(self, col, row):
        for y_cells in range(-1,2):
            for x_cells in range(-1,2):
                x = col + x_cells
                y = row + y_cells
                if x > 0 and y > 0 and x < 99 and y < 99:
                    new_squares[(x, y)] = self.get_square(x, y)
                    check_these_squares += new_squares
                    del new_squares[col, row]
                    return new_squares
    def surrounding_square_counter(self):
        pass
        # counter = 0
        # self.surrounding_square_list_maker()
        # for squares in surrounding_square_list_maker()
        #     if squares.is_alive_or_dead(): #checks rows above and below chosen square
        #         counter += 1
        #     # square = self.get_square(col + x_cells, row + y_cells)
        #     # new_squares_to_check[(col + x_cells, row + y_cells)] = square
        #     # if x_cells == 0:
        #     #     other_square = self.get_square(col + y_cells, row)
        #     #     new_squares_to_check[(col + y_cells, row)] = other_square
        # return counter

if __name__ == "__main__":
	new_game()