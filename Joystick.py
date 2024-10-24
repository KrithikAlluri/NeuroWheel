import pygame
import socket
import time
import math
import ComputerComms

# Initialize Pygame
pygame.init()

# Screen dimensions for Pygame window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Wheelchair representation
wheelchair_radius = 30
wheelchair_x = SCREEN_WIDTH // 2
wheelchair_y = SCREEN_HEIGHT // 2
wheelchair_speed = 5
wheelchair_angle = 0  # Angle in degrees

# Create the Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wheelchair Movement Simulation')

# Setup socket communication to send to the Raspberry Pi
def send_to_computer(arcade_y, arcade_x):
    server_ip = 'COMPUTER_IP'  # Replace with the computer's IP address
    port = 12345  # Ensure this matches the port on the computer side

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, port))
        message = f"{arcade_y},{arcade_x}\n"
        s.sendall(message.encode())
        print(f"Sent to Raspberry Pi: {message.strip()}")

# Map WASD keys to arcade drive values
def map_wasd_to_arcade(keys):
    arcade_y = 2.5  # Neutral (no forward/backward movement)
    arcade_x = 2.5  # Neutral (no turning)

    # Forward/Backward: W to go forward, S to go backward
    if keys[pygame.K_w]:
        arcade_y = 5  # Full forward
    elif keys[pygame.K_s]:
        arcade_y = 0.5  # Full backward

    # Left/Right: A to turn left, D to turn right
    if keys[pygame.K_a]:
        arcade_x = 0.5  # Full left
    elif keys[pygame.K_d]:
        arcade_x = 4.5  # Full right

    return arcade_y, arcade_x

# Function to draw the wheelchair as a circle with text inside
def draw_wheelchair(x, y, angle):
    # Draw the wheelchair as a circle
    pygame.draw.circle(screen, RED, (int(x), int(y)), wheelchair_radius)

    # Draw text inside the circle saadadad(indicating the front of the wheelchair)
    font = pygame.font.Font(None, 24)
    text = font.render('Front', True, BLACK)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

    # Draw the direction the wheelchair is facing (optional)
    front_x = x + wheelchair_radius * math.cos(math.radians(angle))
    front_y = y - wheelchair_radius * math.sin(math.radians(angle))
    pygame.draw.line(screen, BLACK, (x, y), (front_x, front_y), 3)


def display_voltage_values(arcade_y, arcade_x):
    # font = pygame.font.SysFont(None,size = 36)

    # Format the text to show the voltage values for turning and forward movement
    voltage_text = f"Forward: {arcade_y:.1f}V, Turn: {arcade_x:.1f}V"

    # Render the text
    # text_surface = font.render(voltage_text, True, BLACK)
    #
    # # Position the text in the top right corner
    # text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    #
    # # Draw the text on the screen
    # screen.blit(text_surface, text_rect)
    pygame.display.set_caption(voltage_text)


# Function to update the position based on the angle and speed
def update_position(x, y, angle, speed):
    x += speed * math.cos(math.radians(angle))
    y -= speed * math.sin(math.radians(angle))
    return x, y

# Main loop
if __name__ == "__main__":
    clock = pygame.time.Clock()

    try:
        while True:
            # Handle Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Get the current key states
            keys = pygame.key.get_pressed()

            # Map the WASD keys to arcade drive values
            arcade_y, arcade_x = map_wasd_to_arcade(keys)

            # Simulate movement based on arcade values
            if arcade_y > 2.5:  # Move forward
                wheelchair_x, wheelchair_y = update_position(wheelchair_x, wheelchair_y, wheelchair_angle, (arcade_y - 2.5) * wheelchair_speed / 2.5)
            elif arcade_y < 2.5:  # Move backward
                wheelchair_x, wheelchair_y = update_position(wheelchair_x, wheelchair_y, wheelchair_angle, -(2.5 - arcade_y) * wheelchair_speed / 2.5)

            if arcade_x < 2.5:  # Turn left
                wheelchair_angle += 5
            elif arcade_x > 2.5:  # Turn right
                wheelchair_angle -= 5

            # Clear the screen
            screen.fill(WHITE)

            # Draw the wheelchair as a circle with text
            draw_wheelchair(wheelchair_x, wheelchair_y, wheelchair_angle)
            display_voltage_values(arcade_y, arcade_x)

            # Update the display
            pygame.display.update()
            ComputerComms.send_to_rpi((arcade_x), arcade_y)

            # print(arcade_y, arcade_x)

            # Cap the frame rate
            clock.tick(60)

            # Sleep to limit the frequency of sending data
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Program terminated")
        pygame.quit()