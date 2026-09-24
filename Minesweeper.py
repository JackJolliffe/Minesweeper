#new class based minesweeper.py
import pygame
import math
import minesweeper_module as mm
from field_module import Field
from mouse import Mouse
from keyboard import Keyboard
import os


class Game():
    def __init__(self):
        pygame.init()

        #field_setup
        self.tile_width = 26
        self.edge_width = self.tile_width
        self.size_options = [((10, 10), "small"), ((20, 20), "medium"), ((30, 30), "large")]
        self.density_options = [(10, "low_density"), (15, "medium_density"), (20, "high_density")]
        self.field_width, self.field_height = self.size_options[0][0]
        self.density = self.density_options[0][0]
        self.initial_known_value = "plain"
        self.initial_unknown_value = "empty"
        self.bomb = "bomb"
        self.hit_bomb = "hit_bomb"
        self.flag = "flag"

        #button attribute settings
        self.button_width = 2 * self.tile_width
        self.button_height = self.button_width
        self.button_dimensions = (self.button_width, self.button_height)
        self.num_density_buttons = 3
        self.num_size_buttons = 3
        self.num_total_buttons = self.num_density_buttons + self.num_size_buttons

        self.clock = pygame.time.Clock()
        self.fps = 60

        #screen setup
        self.perfect_width, self.perfect_height = mm.calculate_perfect_grid_sizes(self.field_width, self.field_height, self.edge_width, self.tile_width, self.button_width, self.button_height, self.num_total_buttons)
        self.screen_width = self.perfect_width
        self.screen_height = self.perfect_height
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        if 'SDL_VIDEO_WINDOW_POS' in os.environ:
            del os.environ['SDL_VIDEO_WINDOW_POS']
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.title = "New Minesweeper"
        pygame.display.set_caption(self.title)
        self.fullscreen = False
        self.perfect_size = False
        self.screen_width_old = self.screen_width #used to swap from full to normal size
        self.screen_height_old = self.screen_height #used to swap from full to normal size
        self.monitor_width = 1920
        self.monitor_height = 1080


        #game loop setup
        self.running = True
        self.paused = False

        #image importing setup
        self.assets_filename = "asset_names_and_locations.txt"
        self.images = mm.read_assets(self.assets_filename)
        self.image_held = self.images["red"]
        self.image_unheld = self.images["plain"]

        #field creation
        self.field = Field(self.field_width, self.field_height, self.initial_known_value, self.initial_unknown_value, self.bomb, self.hit_bomb, self.flag, self.tile_width, self.edge_width, self.images)
        # self.field.generate_bombs(self.bomb_count)
        self.field.started = False

        #set reveal cheat
        self.reveal = False

        #mouse creation
        self.mouse = Mouse()

        #keyboard creation
        self.keyboard = Keyboard()

        #button creation
        self.generate_buttons()

    def generate_buttons(self):
        self.button_positions = mm.calculate_button_positions(self.tile_width, self.edge_width, self.field.width, self.button_height, self.num_total_buttons)
        self.density_buttons = []
        self.size_buttons = []
        for i in range(0, self.num_density_buttons):
            self.density_buttons.append([pygame.Rect(self.button_positions[i], self.button_dimensions), self.density_options[i][1]])
        for i in range(0, self.num_size_buttons):
            self.size_buttons.append([pygame.Rect(self.button_positions[i + self.num_density_buttons], self.button_dimensions), self.size_options[i][1]])
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE: #resizing pauses the game until the resize is finished
                # Handle window resize
                self.perfect_size = False
                self.fullscreen = False
                self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                self.screen_width, self.screen_height = self.screen.get_size()

            #button down detection
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse.position = pygame.mouse.get_pos()
                # mouse_state = pygame.mouse.get_pressed()
                if event.button == 1:
                    self.mouse.left_clicked = True
                    self.mouse.left_held = True
                if event.button == 3:
                    self.mouse.right_clicked = True
                    self.mouse.right_held = True

            #button up detection
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse.left_held = False
                if event.button == 3:
                    self.mouse.right_held = False

            #key down detection
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.keyboard.r_pressed = True
                    self.keyboard.r_held = True
                if event.key == pygame.K_c:
                    self.keyboard.c_pressed = True
                    self.keyboard.c_held = True
                if event.key == pygame.K_f:
                    self.keyboard.f_pressed = True
                    self.keyboard.f_held = True
                if event.key == pygame.K_s:
                    self.keyboard.s_pressed = True
                    self.keyboard.s_held = True
                if event.key == pygame.K_q:
                    self.running = False

            #keydown detection
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    self.keyboard.r_held = False
                if event.key == pygame.K_c:
                    self.keyboard.c_held = False
                if event.key == pygame.K_f:
                    self.keyboard.f_held = False
                if event.key == pygame.K_s:
                    self.keyboard.s_held = False
    
    def update_game(self):
        self.field.win_check()
        if self.keyboard.r_pressed:
            self.field.width = self.field_width
            self.field.height = self.field_height
            self.field.generate_initial_grid()
            self.generate_buttons()
            self.field.started = False
            self.reveal = False
            self.field.bombless_list = []

        if self.keyboard.c_pressed:
            self.reveal = not self.reveal

        if self.keyboard.f_pressed:
            self.fullscreen = True
            self.perfect_size = False
            os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"#sets the windows top left corner to the top left of the monitor
            self.screen = pygame.display.set_mode((self.monitor_width, self.monitor_height), pygame.RESIZABLE)

        if self.keyboard.s_pressed:
            self.perfect_size = True
            self.fullscreen = False
            self.perfect_width, self.perfect_height = mm.calculate_perfect_grid_sizes(self.field_width, self.field_height, self.edge_width, self.tile_width, self.button_width, self.button_height, self.num_total_buttons)
            # Revert back to a standard bordered window instantly
            os.environ['SDL_VIDEO_CENTERED'] = '1'#sets the window to be centered in the monitor
            if 'SDL_VIDEO_WINDOW_POS' in os.environ:#detects the mandatory position that could be imposed by the fulscreen setting
                del os.environ['SDL_VIDEO_WINDOW_POS']#removes said setting
            self.screen = pygame.display.set_mode((self.perfect_width, self.perfect_height), pygame.RESIZABLE)

        if self.mouse.left_clicked:
            coordinate, error = self.field.tile_from_position(self.mouse.position)
            if error != 1:#if the mouse was on the game grid
                if not self.field.started:#if the game has not started
                    self.field.started = True
                    self.field.generate_bombs(coordinate, self.density)
                    self.field.calc_numbers()
                tile, bomb_check = self.field.reveal_tile(coordinate)
                if bomb_check:#if the tile was a bomb
                    self.field.swap_bomb(coordinate)
                else:
                    self.field.remove_from_bombless_list(coordinate)
                self.field.spread_empty(tile, coordinate)
            else:#if the mouse was not on the game grid
                density_result = mm.determine_button_click(self.density_buttons, self.num_density_buttons, self.mouse.position)
                size_result = mm.determine_button_click(self.size_buttons, self.num_size_buttons, self.mouse.position)
                if density_result[1] != 1:#if a density button was clicked
                    self.density = self.density_options[density_result[0]][0]
                if size_result[1] != 1:#if a size button was clicked
                    self.field_width, self.field_height = self.size_options[size_result[0]][0]
        if self.mouse.right_clicked:
            coordinate, error = self.field.tile_from_position(self.mouse.position)
            if error != 1 and self.field.started:
                self.field.set_flag(coordinate)
            
        #do everything before you reset these things
        self.mouse.left_clicked = False
        self.mouse.right_clicked = False
        self.keyboard.r_pressed = False
        self.keyboard.c_pressed = False
        self.keyboard.f_pressed = False
        self.keyboard.s_pressed = False
    
    def draw_game(self):
        self.screen.blit(self.images["background_image"], (0,0))
        self.field.display_grid(self.screen, self.field.known_grid)
        mm.display_option_buttons(self.screen, self.num_density_buttons, self.images, self.density_buttons)
        mm.display_option_buttons(self.screen, self.num_size_buttons, self.images, self.size_buttons)
        if self.reveal:
            self.field.display_grid(self.screen, self.field.unknown_grid)
        if self.field.won:
            self.field.display_grid(self.screen, self.field.won_grid)
    
    def main(self):
        while self.running:
            self.handle_events()
            self.update_game()
            self.draw_game()
            pygame.display.update()#must update after you display images
            self.clock.tick(self.fps)
        pygame.quit()

game = Game()
game.main()