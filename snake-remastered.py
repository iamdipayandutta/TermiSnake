import curses
import random

# Setup the game window
def setup_window():
    curses.initscr()
    win = curses.newwin(22, 62, 0, 0)  # Window size: 22 rows, 62 cols
    win.keypad(True)  # Enable arrow key input
    curses.noecho()
    curses.curs_set(0)  # Hide cursor
    win.nodelay(True)  # Non-blocking input
    curses.start_color()  # Enable colors

    # Define colors
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Food color
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Border color
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Scoreboard color
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Pause message
    return win

# Function to display Game Over screen with Restart Option
def game_over(win, score):
    win.clear()
    win.border()
    win.addstr(9, 22, " GAME OVER! ", curses.color_pair(2) | curses.A_BOLD)
    win.addstr(11, 23, f"Final Score: {score}", curses.color_pair(4) | curses.A_BOLD)
    win.addstr(13, 17, "Press 'R' to Restart or 'Q' to Quit", curses.color_pair(3))
    win.refresh()

    while True:
        key = win.getch()
        if key == ord('r') or key == ord('R'):
            curses.endwin()  # Reset terminal
            snake_game()  # Restart game
        elif key == ord('q') or key == ord('Q'):
            curses.endwin()
            exit()

# Main Snake Game function
def snake_game():
    win = setup_window()

    # Snake starting position
    snake = [[10, 15], [10, 14], [10, 13]]  # Snake body: head + tail
    food = [random.randint(1, 20), random.randint(1, 60)]  # Initial food position
    win.addch(food[0], food[1], 'X', curses.color_pair(2))  # 'X' as food

    score = 0
    key = curses.KEY_RIGHT  # Start moving right
    speed = 100  # Initial speed

    while True:
        win.clear()
        win.border()  # Draw game border
        win.addstr(0, 20, f" Score: {score} ", curses.color_pair(4) | curses.A_BOLD)
        win.addstr(0, 45, "Press 'P' to Pause", curses.color_pair(3))

        # Display food
        win.addch(food[0], food[1], 'X', curses.color_pair(2))  # 'X' as food

        # Get user input
        new_key = win.getch()
        if new_key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            # Prevent reversing direction (can't go left if moving right, etc.)
            if (new_key == curses.KEY_LEFT and key != curses.KEY_RIGHT) or \
            (new_key == curses.KEY_RIGHT and key != curses.KEY_LEFT) or \
            (new_key == curses.KEY_UP and key != curses.KEY_DOWN) or \
            (new_key == curses.KEY_DOWN and key != curses.KEY_UP):
                key = new_key

        if new_key == ord('p') or new_key == ord('P'):
            win.addstr(10, 20, " PAUSED - Press any key to Resume ", curses.color_pair(5) | curses.A_BOLD)
            win.refresh()
            win.getch()  # Wait for user input to resume

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
        if head in snake or head[0] in [0, 21] or head[1] in [0, 61]:
            game_over(win, score)
            break

        # Move the snake
        snake.insert(0, head)  # Add new head

        # Check if food is eaten
        if head == food:
            score += 10  # Increase score
            food = [random.randint(1, 20), random.randint(1, 60)]  # Generate new food
            win.addch(food[0], food[1], 'X', curses.color_pair(2))  # 'X' as food  
            if speed > 50:
                speed -= 2  # Increase game speed as score increases
        else:
            tail = snake.pop()  # Remove tail
            win.addch(tail[0], tail[1], ' ')  # Erase tail

        # Draw snake
        for i, segment in enumerate(snake):
            char = 'O' if i == 0 else 'o'  # Head = 'O', Body = 'o'
            win.addch(segment[0], segment[1], char, curses.color_pair(1))

        win.refresh()
        win.timeout(speed)  # Control speed

# Run the game
if __name__ == "__main__":
    snake_game()
