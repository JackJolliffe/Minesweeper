import random as r
from math import floor

class Field():
    def __init__(self, width, height, plain, empty, bomb, hit_bomb, flag, tile_width, edge_width, images):
        self.width = width
        self.height = height
        self.empty = empty
        self.plain = plain
        self.bomb = bomb
        self.hit_bomb = hit_bomb
        self.flag = flag
        self.tile_width = tile_width
        self.edge_width = edge_width
        self.images = images
        self.started = False
        self.known_grid = []
        self.unknown_grid = []
        self.won_grid = []
        self.bombless_list = []
        self.generate_initial_grid()

    def generate_initial_grid(self):
        self.known_grid = [[self.plain for i in range(self.height)] for j in range(self.width)]
        self.unknown_grid = [[self.empty for i in range(self.height)] for j in range(self.width)]
        self.won_grid = [[self.empty for i in range(self.height)] for j in range(self.width)]

    def generate_bombs(self, coordinates, density):
        self.bombless_list = []
        for i in range(0, self.width):
            for j in range(0, self.height):
                self.bombless_list.append([i, j])

        #stopping 3x3 around "spawn" from being bombs
        x, y = coordinates
        xstart, xend, ystart, yend = self.calc_bounds(x, y)
        for i in range(xstart, xend+1):
            for j in range(ystart, yend+1):
                self.bombless_list.remove([i, j])

        bomb_count = self.gen_bomb_count(density)
        for i in range(0, bomb_count):
            element_num = r.randint(0,len(self.bombless_list) - 1)#randint can generate the final number, so "-1" is needed at the end
            position = self.bombless_list.pop(element_num)
            self.unknown_grid[position[0]][position[1]] = self.bomb
            self.won_grid[position[0]][position[1]] = self.flag

    def gen_bomb_count(self, density):
        volume = self.width * self.height
        bomb_count = floor((density/100)*volume)
        return(bomb_count)

    def calc_numbers(self):
        for x in range(0,self.width):
            for y in range(0, self.height):
                if self.unknown_grid[x][y] != self.bomb:
                    num_bombs = self.calc_num_bombs(x, y)
                    self.unknown_grid[x][y] = str(num_bombs) if num_bombs != 0 else self.empty

    def calc_num_bombs(self, x, y):
        xstart, xend, ystart, yend = self.calc_bounds(x, y)
        num_bombs = 0

        for i in range(xstart, xend+1):
            for j in range(ystart, yend+1):
                num_bombs = num_bombs + 1 if self.unknown_grid[i][j] == self.bomb else num_bombs
        return(num_bombs)

    def display_grid(self, screen, grid):#displays the grid given as an argument
        for i in range(0, self.width):
            for j in range(0, self.height):
                x = i*self.tile_width + self.edge_width
                y = j*self.tile_width + self.edge_width
                screen.blit(self.images[grid[i][j]], (x, y))

    def tile_from_position(self, position):#calculates the coordinate of the tile form the mouse position
        x = floor((position[0] - self.edge_width)/self.tile_width)
        y = floor((position[1] - self.edge_width)/self.tile_width)

        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:#i.e. x or y or both are out of bounds
            return([x, y], 1)
        return([x, y], 0)

    #when clicked on the contents of tile grid is set to that of the corresponding tile in the unknown grid
    def reveal_tile(self, coordinate):
        x = coordinate[0]
        y = coordinate[1]
        tile = self.unknown_grid[x][y]
        if self.known_grid[x][y] != self.flag:
            self.known_grid[x][y] = tile
        if tile == self.bomb:
            return(tile, 1)
        return(tile, 0)

    def spread_empty(self, tile, coordinate):#if an empty tile is clicked on all adjacent empty tiles are revealed.
        if tile == self.empty:
            x = coordinate[0]
            y = coordinate[1]
            xstart, xend, ystart, yend = self.calc_bounds(x, y)

            for i in range(xstart, xend+1):
                for j in range(ystart, yend+1):
                    if self.known_grid[i][j] != self.unknown_grid[i][j]:
                        self.known_grid[i][j] = self.unknown_grid[i][j]
                        self.remove_from_bombless_list([i,j])
                        if self.known_grid[i][j] == self.empty:
                            self.spread_empty(self.empty, (i, j))

    def calc_bounds(self, x, y):
        xstart = x-1
        xend   = x+1
        ystart = y-1
        yend   = y+1

        if x == 0:
            xstart = x
        elif x == self.width-1:
            xend = x
        if y == 0:
            ystart = y
        elif y == self.height-1:
            yend = y
        return(xstart, xend, ystart, yend)

    def set_flag(self, coordinate):
        x = coordinate[0]
        y = coordinate[1]
        if self.known_grid[x][y] == self.plain:
            self.known_grid[x][y] = self.flag
        elif self.known_grid[x][y] == self.flag:
            self.known_grid[x][y] = self.plain

    def swap_bomb(self, coordinates):
        x, y = coordinates
        self.known_grid[x][y] = self.hit_bomb

    def win_check(self):
        self.won = True if (not self.bombless_list and self.started) else False

    def remove_from_bombless_list(self, coordinate):
        if coordinate in self.bombless_list:
            self.bombless_list.remove(coordinate)