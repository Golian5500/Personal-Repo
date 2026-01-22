import tkinter as tk
import time
import random
# Game constants
WIDTH = 400
HEIGHT = 400
SNAKE_SIZE = 10
SPEED = 100  # milliseconds between moves

# Define the snake's body and food
snake_body = [(100, 100), (150, 100), (200, 100)]
food = (50, 50)

# Game variables
x, y = 100, 100
direction = 'RIGHT'
game_over = False

# Create the main window
root = tk.Tk()
root.title("Snake Game")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Draw the snake and food on the canvas
def draw_snake():
    canvas.delete("all")  # Clear canvas
    for segment in snake_body:
        canvas.create_rectangle(
            segment[0] - SNAKE_SIZE//2, segment[1] - SNAKE_SIZE//2,
            segment[0] + SNAKE_SIZE//2, segment[1] + SNAKE_SIZE//2,
            fill="green", outline="white"
        )
    canvas.create_oval(
        food[0] - 5, food[1] - 5,
        food[0] + 5, food[1] + 5,
        fill="red"
    )

def move_snake():
    global x, y, direction, snake_body, food, game_over

    # Move the snake
    if direction == 'UP':
        y -= SNAKE_SIZE
    elif direction == 'DOWN':
        y += SNAKE_SIZE
    elif direction == 'LEFT':
        x -= SNAKE_SIZE
    elif direction == 'RIGHT':
        x += SNAKE_SIZE

    # Check for collision with walls or self
    if (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT) or (x, y) in snake_body:
        game_over = True
        return

    # Add new head
    snake_body.insert(0, (x, y))

    # Check if snake ate food
    if (x, y) == food:
        # Generate new food
        food = (random.randint(0, WIDTH//SNAKE_SIZE - 1) * SNAKE_SIZE,
                random.randint(0, HEIGHT//SNAKE_SIZE - 1) * SNAKE_SIZE)
        # Don't remove tail (grow!)
    else:
        # Remove tail
        snake_body.pop()

    # Draw the new frame
    draw_snake()

    # Check if game over
    if game_over:
        canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over!", fill="white", font=("Arial", 24))
        root.after(2000, lambda: root.destroy())  # Close after 2 seconds

# Key press handler
def change_direction(event):
    global direction
    if event.keysym == 'Up' and direction != 'DOWN':
        direction = 'UP'
    elif event.keysym == 'Down' and direction != 'UP':
        direction = 'DOWN'
    elif event.keysym == 'Left' and direction != 'RIGHT':
        direction = 'LEFT'
    elif event.keysym == 'Right' and direction != 'LEFT':
        direction = 'RIGHT'

# Bind keys
root.bind('<Up>', change_direction)
root.bind('<Down>', change_direction)
root.bind('<Left>', change_direction)
root.bind('<Right>', change_direction)

# Start the game loop
def game_loop():
    move_snake()
    root.after(SPEED, game_loop)  # Call again after delay

# Start the game
draw_snake()
game_loop()

# Run the main loop
root.mainloop()
