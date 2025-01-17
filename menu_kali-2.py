#!/usr/bin/env python
import sys, os, subprocess, time, pygame, socket
from pygame.locals import *
from subprocess import *

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

# Initialize pygame modules individually (to avoid ALSA errors) and hide mouse
pygame.font.init()
pygame.display.init()
pygame.mouse.set_visible(0)


# define function for printing text in a specific place with a specific width and height with a specific colour and border
def make_button(text, xpo, ypo, height, width, colour):
    pygame.draw.rect(screen, tron_regular, (xpo - 10, ypo - 10, width, height), 3)
    pygame.draw.rect(screen, tron_light, (xpo - 9, ypo - 9, width - 1, height - 1), 1)
    pygame.draw.rect(screen, tron_regular, (xpo - 8, ypo - 8, width - 2, height - 2), 1)
    font = pygame.font.Font(None, 42)
    label = font.render(str(text), 1, (colour))
    screen.blit(label, (xpo, ypo))


# define function for printing text in a specific place with a specific colour
def make_label(text, xpo, ypo, fontsize, colour):
    font = pygame.font.Font(None, fontsize)
    label = font.render(str(text), 1, (colour))
    screen.blit(label, (xpo, ypo))


# define function that checks for touch location
def on_touch():
    # get the position that was touched
    touch_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    #  x_min                 x_max   y_min                y_max
    # button 1 event
    if 30 <= touch_pos[0] <= 240 and 105 <= touch_pos[1] <= 160:
        button(1)
    # button 2 event
    if 260 <= touch_pos[0] <= 470 and 105 <= touch_pos[1] <= 160:
        button(2)
    # button 3 event
    if 30 <= touch_pos[0] <= 240 and 180 <= touch_pos[1] <= 235:
        button(3)
    # button 4 event
    if 260 <= touch_pos[0] <= 470 and 180 <= touch_pos[1] <= 235:
        button(4)
    # button 5 event
    if 30 <= touch_pos[0] <= 240 and 255 <= touch_pos[1] <= 310:
        button(5)
    # button 6 event
    if 260 <= touch_pos[0] <= 470 and 255 <= touch_pos[1] <= 310:
        button(6)


# Get Your External IP Address
def get_ip():
    ip_msg = "Not connected"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('<broadcast>', 0))
        ip_msg = " IP: " + s.getsockname()[0]
    except Exception:
        pass
    return ip_msg


# Restart Raspberry Pi
def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output


# Shutdown Raspberry Pi
def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output


def get_temp():
    command = "vcgencmd measure_temp"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output


def run_cmd(cmd):
    process = Popen(cmd.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output


# Define each button press action
def button(number):
    if number == 1:
        # Kismet
        pygame.quit()
        subprocess.call("/usr/bin/sudo -u pi /usr/bin/kismet", shell=True)
        os.execv(__file__, sys.argv)

    if number == 2:
        # SDR-Scanner
        pygame.quit()
        prog = "/bin/bash " + os.environ["MENUDIR"] + "sdr-scanner.sh"
        run_cmd(prog)
        os.execv(__file__, sys.argv)

    if number == 3:
        # shutdown
        pygame.quit()
        shutdown()
        sys.exit()

    if number == 4:
        # reboot
        screen.fill(black)
        font = pygame.font.Font(None, 72)
        label = font.render("Rebooting. .", 1, (white))
        screen.blit(label, (40, 120))
        pygame.display.flip()
        pygame.quit()
        restart()
        sys.exit()

    if number == 5:
        # Previous page
        pygame.quit()
        page = os.environ["MENUDIR"] + "menu_kali-1.py"
        os.execvp("python", ["python", page])
        sys.exit()

    if number == 6:
        # Next page
        pygame.quit()
        page = os.environ["MENUDIR"] + "menu_kali-3.py"
        os.execvp("python", ["python", page])
        sys.exit()


# colors    R    G    B
white = (255, 255, 255)
tron_whi = (189, 254, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
tron_blu = (0, 219, 232)
black = (0, 0, 0)
cyan = (50, 255, 255)
magenta = (255, 0, 255)
yellow = (255, 255, 0)
tron_yel = (255, 215, 10)
orange = (255, 127, 0)
tron_ora = (255, 202, 0)

# Tron theme orange
## tron_regular = tron_ora
## tron_light = tron_yel
## tron_inverse = tron_whi

# Tron theme blue
tron_regular = tron_blu
tron_light = tron_whi
tron_inverse = tron_yel

# Set up the base menu you can customize your menu with the colors above

# set size of the screen
size = width, height = 480, 320
screen = pygame.display.set_mode(size)

# Background Color
screen.fill(black)

# Outer Border
pygame.draw.rect(screen, tron_regular, (0, 0, 479, 319), 8)
pygame.draw.rect(screen, tron_light, (2, 2, 479 - 4, 319 - 4), 2)

# Buttons and labels
# First Row Label
make_label(get_ip(), 32, 30, 48, tron_inverse)
# Second Row buttons 1 and 2
make_button("     Kismet", 30, 105, 55, 210, tron_light)
make_button(" SDR-Scanner", 260, 105, 55, 210, tron_light)
# Third Row buttons 3 and 4
make_button("   Shutdown", 30, 180, 55, 210, tron_light)
make_button("      Reboot", 260, 180, 55, 210, tron_light)
# Fourth Row Buttons
make_button("         <<<", 30, 255, 55, 210, tron_light)
make_button("         >>>", 260, 255, 55, 210, tron_light)

# While loop to manage touch screen inputs
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            on_touch()

        # ensure there is always a safe way to end the program if the touch screen fails
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    pygame.display.update()
    ## Reduce CPU utilisation
    time.sleep(0.1)
