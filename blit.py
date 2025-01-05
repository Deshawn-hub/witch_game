import random
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Define a list of colors to choose from
colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)]

dt = 0

def keys(player_pos,dt):
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_RIGHT]:
        player_pos.x += 300 * dt

# Define the Square class
class Square(pygame.sprite.Sprite):
    def __init__(self, col, x, y,height,width):
        super().__init__()
        self.image = pygame.Surface((height,width))
        self.image.fill(col)  # Fill with RGB color
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.y_velocity = 0
       
        


    def update(self, all_squares):
        # Apply gravity
        self.y_velocity += 0.03  # Gravity strength
        self.rect.y += self.y_velocity  # Apply velocity to the y position

        # Check for collision with the bottom of the screen
        if self.rect.bottom >= 720:  # Screen height is 720
            self.rect.bottom = 720  # Snap to the bottom of the screen
            self.y_velocity = 0  # Stop moving

        # Stop at left or right of screen
        if self.rect.left <= 0:  
            self.rect.left = 0
        elif self.rect.right >= 1280:  # Right boundary
            self.rect.right = 1280

        # Check for collisions with other squares
        for square in all_squares:
            if square == self:
                continue  # Skip checking against itself

            # If the current square is falling and collides with another square
            if self.rect.colliderect(square.rect) and self.rect.bottom > square.rect.top:
                self.rect.bottom = square.rect.top  # Stop at the top of the other square
                self.y_velocity = 0  # Stop movin

                if self.get_color() == square.get_color():
                    all_squares.remove(self)
                    all_squares.remove(square)
                    

    def get_color(self):
        # Get the color of the top-left pixel (since the entire surface is filled with the same color)
        return self.image.get_at((0, 0))


    
    
     

# Create a sprite group
squares = pygame.sprite.Group()
shape_width = [30,50,70,80] 
shape_height = [10,30,50,70,80]  

# Flag to control square creation
can_create_new_square = True

# Main loop
while running:
    dt = clock.tick(60) / 1000
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if all squares have stopped
    squared_stop = all(square.rect.bottom >= 710 or square.y_velocity == 0 for square in squares)

    # Create a new square if the previous one has stopped and the flag is True
    if squared_stop and can_create_new_square:
        new_square = Square(random.choice(colours), random.randint(100, 1180), 0,random.choice(shape_height),random.choice(shape_width))
        current_square = new_square
        squares.add(new_square)
        can_create_new_square = False  # Prevent creating another square until this one stops
        

    # Reset the flag if the new square has stopped
    if not can_create_new_square and squared_stop:
        can_create_new_square = True

    if current_square:
        keys(current_square.rect,dt)

    #if len(squares) >= 3:
     #   current_square.y_velocity +=1 

        

    

    # Clear the screen
    screen.fill('cyan')

    # Update squares
    squares.update(squares)

    # Draw the sprites
    squares.draw(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()