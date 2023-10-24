import pygame
import sys
import random

def display_image(image_path_open, image_path_closed):
    # Initialize Pygame
    pygame.init()

    # Set the dimensions of the window
    window_size = (480, 800)
    screen = pygame.display.set_mode(window_size, pygame.NOFRAME)

    # Load the images
    image_open = pygame.image.load(image_path_open)
    image_closed = pygame.image.load(image_path_closed)

    # Start with eyes open
    current_image = image_open

    # Create a clock object to manage time
    clock = pygame.time.Clock()

    # Set the initial next blink time
    next_blink_time = pygame.time.get_ticks() + random.randint(2000, 5000)  # 2 to 5 seconds

    # Wait for user to quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        current_time = pygame.time.get_ticks()
        if current_time >= next_blink_time:
            current_image = image_closed  # Close eyes
            screen.blit(current_image, (0, 0))
            pygame.display.flip()

            next_blink_time = current_time + random.randint(50, 150)  # 0.1 to 0.5 seconds

            while pygame.time.get_ticks() < next_blink_time:
                pass  # Busy wait (this can be replaced with other processing)

            current_image = image_open  # Open eyes
            next_blink_time = current_time + random.randint(2000, 5000)  # 2 to 5 seconds

        # Blit the current image and update the display
        screen.blit(current_image, (0, 0))
        pygame.display.flip()

        # Limit the frame rate to reduce CPU usage
        clock.tick(60)  # 60 frames per second

    # Quit Pygame
    pygame.quit()
    sys.exit()

# Usage
if __name__ == "__main__":
    image_path_open = 'Chai Faces/Smile.png'
    image_path_closed = 'Chai Faces/Blink.png'
    display_image(image_path_open, image_path_closed)
