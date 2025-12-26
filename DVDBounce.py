import pygame
import sys
import os
import ctypes
import random

# Initialize pygame
pygame.init()

# ========================
# LOGO RECOLORING FUNCTIONS
# ========================
def recolor_black_logo(image, color):
    recolored = image.copy()
    arr = pygame.surfarray.pixels3d(recolored)

    black = (
        (arr[:, :, 0] == 0) &
        (arr[:, :, 1] == 0) &
        (arr[:, :, 2] == 0)
    )

    arr[black] = color
    del arr  # unlock the surface
    return recolored

def pick_color():
    return (
        random.randint(50, 255),
        random.randint(50, 255),
        random.randint(50, 255)
    )


# =========================
# SCREEN SETTINGS
# =========================
WINDOWED_SIZE = (800, 600)
WIDTH, HEIGHT = WINDOWED_SIZE
fullscreen = False

screen = pygame.display.set_mode(WINDOWED_SIZE)
pygame.display.set_caption("DVD Logo Screensaver")
print('Starting DVDBounce — screen:', WIDTH, 'x', HEIGHT)

# Clock for controlling frame rate
clock = pygame.time.Clock()
frames = 0

# =========================
# LOGO SETTINGS
# =========================
logo_width, logo_height = 160, 80
logo_x, logo_y = 10, 10
speed_x, speed_y = 4, 4

# =========================
# FULLSCREEN TOGGLE FUNCTION
# =========================

def get_screen_resolution():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()  # Make sure we get full resolution
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    return width, height

def toggle_fullscreen():
    global screen, WIDTH, HEIGHT, fullscreen

    fullscreen = not fullscreen

    if fullscreen:
        WIDTH, HEIGHT = get_screen_resolution()
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    else:
        WIDTH, HEIGHT = WINDOWED_SIZE
        screen = pygame.display.set_mode(WINDOWED_SIZE)
    print('Toggled fullscreen:', fullscreen, 'screen:', WIDTH, 'x', HEIGHT)

def rescale_logo():

    # Scale bigger in windowed fullscreen, normal in windowed mode
    if fullscreen:
        # Windowed fullscreen — make icon bigger
        new_width, new_height = int(160 * 5), int(80 * 5)
    else:
        # Normal windowed — original size
        new_width, new_height = 160, 80

    logo_width, logo_height = new_width, new_height

    # Rescale the logo image if available
    try:
        logo_image_scaled = pygame.image.load(logo_path).convert_alpha()
        logo_image = pygame.transform.smoothscale(logo_image_scaled, (logo_width, logo_height))
    except Exception:
        logo_image = None
        

# =========================
# LOAD LOGO IMAGE
# =========================
script_dir = os.path.dirname(__file__)
logo_path = os.path.join(script_dir, 'dvd_logo.png')
logo_image = None

try:
    logo_image = pygame.image.load(logo_path).convert_alpha()
    logo_image = pygame.transform.smoothscale(logo_image, (logo_width, logo_height))
except Exception as e:
    print(f"Warning: could not load logo image at {logo_path}: {e}")
    logo_image = None

if logo_image:
    print(f"Loaded logo image: {logo_path} (scaled to {logo_width}x{logo_height})")
    original_logo = logo_image.copy()
else:
    print("No logo image found; using rectangle instead")
    original_logo = None




# =========================
# LOAD SOUND
# =========================
ding_sound = None
ding_path = os.path.join(script_dir, 'ding.mp3')

try:
    pygame.mixer.init()
    if os.path.exists(ding_path):
        ding_sound = pygame.mixer.Sound(ding_path)
except Exception as e:
    print(f"Warning: sound disabled: {e}")
    ding_sound = None

# =========================
# COLORS
# =========================
logo_color = (255, 255, 255)
background_color = (30, 144, 255)

# =========================
# MAIN LOOP
# =========================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                toggle_fullscreen()

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Move logo
    logo_x += speed_x
    logo_y += speed_y

    hit_x = False
    hit_y = False

    # Horizontal bounce
    if logo_x <= 0:
        logo_x = 0
        speed_x *= -1
        hit_x = True
    elif logo_x + logo_width >= WIDTH:
        logo_x = WIDTH - logo_width
        speed_x *= -1
        hit_x = True

    # Vertical bounce
    if logo_y <= 0:
        logo_y = 0
        speed_y *= -1
        hit_y = True
    elif logo_y + logo_height >= HEIGHT:
        logo_y = HEIGHT - logo_height
        speed_y *= -1
        hit_y = True

    # Corner hit sound
    if hit_x and hit_y:
        print(f"Corner hit at ({logo_x}, {logo_y})")
        if ding_sound:
            try:
                ding_sound.play()
            except Exception:
                pass

    if (hit_x or hit_y) and original_logo:
        logo_image = recolor_black_logo(original_logo, pick_color())

    # =========================
    # BACKGROUND COLOR RENDERING
    # =========================

    screen.fill(background_color)

    # =========================
    # LOGO RENDERING
    # =========================
    if logo_image:
        screen.blit(logo_image, (logo_x, logo_y))
    else:
        pygame.draw.rect(
            screen, logo_color,
            (logo_x, logo_y, logo_width, logo_height)
        )

    pygame.display.flip()

    frames += 1
    clock.tick(60)
