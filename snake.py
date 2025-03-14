import curses
import random

# Initialize the game window
def setup_window():
    curses.initscr()
    win = curses.newwin(20, 60, 0, 0)  # Create a window (height=20, width=60)
    win.keypad(True)  # Enable arrow key inputs
    curses.noecho()
    curses.curs_set(0)  # Hide cursor
    win.border(0)  # Add border
    win.nodelay(True)  # Non-blocking input
    return win

# Main snake game function
def snake_game():
    win = setup_window()

    # Snake starting position
    snake = [[10, 15], [10, 14], [10, 13]]  # Initial snake size (head + body)
    food = [random.randint(1, 18), random.randint(1, 58)]  # Food position
    win.addch(food[0], food[1], '*')

    # Initial movement direction (right)
    key = curses.KEY_RIGHT

    while True:
        win.border(0)
        win.addch(food[0], food[1], '*')  # Keep food displayed

        # Get user input
        new_key = win.getch()
        key = key if new_key == -1 else new_key  # Ignore invalid keys

        # Compute next head position
        head = snake[0][:]
        if key == curses.KEY_UP:
            head[0] -= 1
        elif key == curses.KEY_DOWN:
            head[0] += 1
        elif key == curses.KEY_LEFT:
            head[1] -= 1
        elif key == curses.KEY_RIGHT:
            head[1] += 1

        # Check for collision with walls or itself
        if head in snake or head[0] in [0, 19] or head[1] in [0, 59]:
            break

        # Add new head
        snake.insert(0, head)

        # Check if food is eaten
        if head == food:
            food = [random.randint(1, 18), random.randint(1, 58)]  # Generate new food
            win.addch(food[0], food[1], '*')
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')  # Remove last segment

        win.addch(snake[0][0], snake[0][1], '#')  # Draw snake's new head
        win.timeout(100)  # Control game speed

    # Cleanup on game over
    curses.endwin()
    print("Game Over!")

# Run the game
if __name__ == "__main__":
    snake_game()
