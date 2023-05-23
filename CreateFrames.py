import os
import math as maths
import pygame

pygame.init()

FRAMES_PATH = "./frames"

FRAME_SIZE = (1920*2, 1080*2)
SCALE_FACTOR = 2

CIRCLE_LINE_THICKNESS = 10 * SCALE_FACTOR
CIRCLE_CENTRE_RADIUS = 10 * SCALE_FACTOR
POINTS_GAP = 300 * SCALE_FACTOR
POINTS_RADIUS = 10 * SCALE_FACTOR
INFOLINE_THICKNESS = 5 * SCALE_FACTOR
CIRCLE_COLOUR = pygame.Color(200, 30, 30)
CIRCLE_CENTRE_COLOUR = pygame.Color(150, 170, 150)
POINT_COLOUR = pygame.Color(220, 220, 220)
BACKGROUND_COLOUR = pygame.Color(15, 20, 15)
INFOLINE_COLOUR = pygame.Color(150, 170, 150, 150)
TEXT_COLOUR = pygame.Color(150, 170, 150, 150)

# How big the gap between points is stated to be in the animation
STATED_GAP_SIZE = 2

FONT_SIZE = 60 * SCALE_FACTOR
font = pygame.font.SysFont("cambriamath", int(FONT_SIZE))

def create_frames(initial_x, final_x, step):
    """Produces the circle animation video's frames and saves them to the frames directory

    Takes in an initial and final x displacement of the centre of the circle from the
    points. step is x movement to the right in each frame.
    """
    for frame_num in range(int((final_x - initial_x) / step) + 1):
        circle_x = initial_x + frame_num * step
        frame_surface = create_frame(circle_x)
        save_frame(frame_surface, frame_num)


def save_frame(surface, frame_num):
    """saves surface as image in frames directory with name frame + [frame_num]."""
    if not os.path.exists(FRAMES_PATH):
        os.makedirs(FRAMES_PATH)

    pygame.image.save(surface, FRAMES_PATH + "/frame" + str(frame_num) + ".jpg")

def create_frame(x):
    """Creates a frame where the circle's centre has an x displacement of x from the points"""
    surface = pygame.Surface(FRAME_SIZE)
    surface.fill(BACKGROUND_COLOUR)
    frame_centre = (FRAME_SIZE[0] / 2, FRAME_SIZE[1] / 2)

    # Get the points on the frame
    top_point_centre = (frame_centre[0],
                        frame_centre[1] - (POINTS_GAP / 2))
    bottom_point_centre = (frame_centre[0],
                            frame_centre[1] + (POINTS_GAP / 2))
    circle_centre = (frame_centre[0] + x , frame_centre[1])

    circle_radius = calculate_radius(x)
    # Draw the circle
    draw_circle(surface, circle_centre, circle_radius)

    # Draw the measurement lines
    draw_infolines(surface, top_point_centre, bottom_point_centre, circle_centre)

    # Draw the numbers
    draw_text(surface, top_point_centre, bottom_point_centre, circle_centre, circle_radius)

    # Draw circle centre
    pygame.draw.circle(surface, CIRCLE_CENTRE_COLOUR, circle_centre,
                        CIRCLE_CENTRE_RADIUS)

    # Draw the two points
    pygame.draw.circle(surface, POINT_COLOUR, top_point_centre,
                        POINTS_RADIUS)
    pygame.draw.circle(surface, POINT_COLOUR, bottom_point_centre,
                        POINTS_RADIUS)

    return surface


def draw_circle(surface, centre, radius):
    """Draws the circle"""
    pygame.draw.circle(surface, CIRCLE_COLOUR, centre,
                        int(radius), int(CIRCLE_LINE_THICKNESS))


def draw_infolines(surface, top_point_centre, bottom_point_centre, circle_centre):
    """Draws the infolines to the surface"""
    # Dawing lines Must be done on a separate surface for transparency
    lines_surface = pygame.Surface(FRAME_SIZE, pygame.SRCALPHA)
    # Draw line between points
    pygame.draw.line(lines_surface, INFOLINE_COLOUR, top_point_centre, bottom_point_centre, int(INFOLINE_THICKNESS))
    # Draw Line from top point to centre of circle
    pygame.draw.line(lines_surface, INFOLINE_COLOUR, top_point_centre, circle_centre, int(INFOLINE_THICKNESS))
    # Draw horizontal line from points to centre of circle
    pygame.draw.line(lines_surface, INFOLINE_COLOUR, (top_point_centre[0], circle_centre[1]), circle_centre, int(INFOLINE_THICKNESS))
    surface.blit(lines_surface, (0, 0))

def draw_text(surface, top_point_centre, bottom_point_centre, circle_centre, radius):
    """Draws text with information about distances to the surface"""
    # Must be done on separate surface for transparency
    text_surface = pygame.Surface(FRAME_SIZE, pygame.SRCALPHA)
    draw_point_to_point_text(text_surface, top_point_centre, bottom_point_centre, circle_centre)
    draw_horizontal_distance_text(text_surface, top_point_centre, bottom_point_centre, circle_centre)
    draw_radius_text(text_surface, top_point_centre, bottom_point_centre, circle_centre, radius)
    surface.blit(text_surface, (0, 0))


def draw_point_to_point_text(surface, top_point_centre, bottom_point_centre, circle_centre):
    """Draws the text displaying the distance from point to point in an appropriate place"""
    text = font.render(str(STATED_GAP_SIZE), True, TEXT_COLOUR)
    # Depending on which side the circle is, the x offset will be different
    x_offset_from_centre = maths.copysign(text.get_rect().width/2 + 15*SCALE_FACTOR, top_point_centre[0] - circle_centre[0])
    pos = (top_point_centre[0] - text.get_rect().width/2 + x_offset_from_centre, 
        (top_point_centre[1] + bottom_point_centre[1])/2 - text.get_rect().height/2)
    surface.blit(text, pos)


def draw_horizontal_distance_text(surface, top_point_centre, bottom_point_centre, circle_centre):
    """Draws the text indicating the horizontal distance from the centre to the points in an appropriate position"""
    actual_distance = circle_centre[0] - top_point_centre[0]
    # Stated distance is the distance that will be displayed.
    stated_distance = "{:.1f}".format(STATED_GAP_SIZE / POINTS_GAP * abs(actual_distance))
    text = font.render(stated_distance, True, TEXT_COLOUR)
    # Text must shift towards centre of the circle
    x_offset_from_centre = clamp(actual_distance/2, -300*SCALE_FACTOR, 300*SCALE_FACTOR)
    # Text must be below line, so offset in y
    y_offset_from_centre = 20*SCALE_FACTOR 
    pos = (top_point_centre[0] - text.get_rect().width/2 + x_offset_from_centre, 
        (top_point_centre[1] + bottom_point_centre[1])/2 + y_offset_from_centre)
    surface.blit(text, pos)


def draw_radius_text(surface, top_point_centre, bottom_point_centre, circle_centre, radius):
    """Draws the text indicating the radius in an appropriate position"""
    # Stated radius is the radius that will be displayed
    stated_radius = "{:.1f}".format(STATED_GAP_SIZE / POINTS_GAP * radius)
    text = font.render(stated_radius, True, TEXT_COLOUR)
    # Text is shifted towards the direction of the centre of the circle
    x_offset_from_centre = clamp((circle_centre[0] - top_point_centre[0])/2, -300*SCALE_FACTOR, 300*SCALE_FACTOR)
    # x_pos_hooked_to is the x position that the text is meant to be 'attached' to
    x_pos_hooked_to = top_point_centre[0] + x_offset_from_centre
    # Get the y of the radius line at the point that the text is 'hooked' to, so that we can put the text above it
    try:
        y_of_radius_at_x = (top_point_centre[1] - circle_centre[1]) * abs((x_pos_hooked_to - circle_centre[0])/(top_point_centre[0] - circle_centre[0]))
    except ZeroDivisionError:
        y_of_radius_at_x = top_point_centre[1] - circle_centre[1]
    # Set the y position so that the text is above the radius line
    y_pos = (top_point_centre[1] + bottom_point_centre[1])/2 + y_of_radius_at_x - text.get_rect().height - 20*SCALE_FACTOR
    surface.blit(text, (x_pos_hooked_to - text.get_rect().width/2, y_pos))


def calculate_radius(x):
    """Returns the radius of the circle that should be drawn where the circle's centre has an x displacement of x from the points"""
    return maths.sqrt(x * x + (POINTS_GAP / 2) * (POINTS_GAP / 2))


def clamp(val, min_val, max_val):
    """if val is below min, returns min. If it is above max, returns max. Otherwise returns val"""
    return max(min(val, max_val), min_val)