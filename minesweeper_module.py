#new_minesweeper_module.py
import pygame
from math import floor

def read_assets(filename):
    images = {}
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            # skip empty lines or comments
            if not line or line.startswith("#"):
                continue

            key, path = line.split(maxsplit=1)#I have left the seperator unspecified so it is a space by default

            image = pygame.image.load(path).convert_alpha()
            images[key] = image

    return images

def display_field(screen, images, field):
    for i in range(0, field.width):
        for j in range(0, field.height):
            x = i*field.tile_width + field.edge_width
            y = j*field.tile_width + field.edge_width
            screen.blit(images[field.unknown_grid[i][j]], (x, y))

def display_mouse_states(screen, mouse, image_held, image_unheld, screen_width, screen_height, edge_width, tile_width):
    left_x = screen_width - edge_width - 2*tile_width
    right_x = screen_width - edge_width - tile_width
    y = screen_height - 2*edge_width

    if mouse.left_held:
        screen.blit(image_held, (left_x, y))
    else:
        screen.blit(image_unheld, (left_x, y))

    if mouse.right_held:
        screen.blit(image_held, (right_x, y))
    else:
        screen.blit(image_unheld, (right_x, y))

def calculate_button_positions(tile_width, edge_width, field_width, button_height, num_buttons):
    x = (1 * edge_width + (field_width + 1) * tile_width)
    y_0 = edge_width
    position_list = []
    for i in range(0,num_buttons):
        y = y_0 + i*(tile_width + button_height)
        position_list.append((x,y))
    return(position_list)

def determine_button_click(buttons, num_buttons, mouse_position):
    for i in range(0, num_buttons):
        if buttons[i][0].collidepoint(mouse_position):
            return(i,0)
    return(0, 1)

def gen_bomb_count(dimensions, percentage):
    volume = dimensions[0] * dimensions[1]
    bomb_count = floor((percentage/100)*volume)
    return(bomb_count)

def display_option_buttons(screen, num_buttons, images, buttons):
    for i in range(0, num_buttons):
        screen.blit(images[buttons[i][1]], buttons[i][0].topleft)

def calculate_perfect_grid_sizes(width, height, edge_width, tile_width, button_width, button_height, num_total_buttons):
    perfect_width = tile_width * width + 3 * edge_width + button_width
    perfect_height_candidate_0 = tile_width * height + 2 * edge_width
    perfect_height_candidate_1 = num_total_buttons * (button_height + edge_width) + edge_width
    perfect_height = max(perfect_height_candidate_0, perfect_height_candidate_1)
    return(perfect_width, perfect_height)