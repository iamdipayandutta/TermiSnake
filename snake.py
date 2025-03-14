import curses
import random

def setup_window():
    curses.initscr()
    win = curses.newwin(20, 60, 0, 0) 
    win.keypad(True) 
    curses.noecho()
    curses.curs_set(0) 
    win.border(0) 
    win.nodelay(True)
    return win


def snake_game():
    win = setup_window()

    snake = [[10, 15], [10, 14], [10, 13]] 
    food = [random.randint(1, 18), random.randint(1, 58)] 
    win.addch(food[0], food[1], '*')

    key = curses.KEY_RIGHT

    while True:
        win.border(0)
        win.addch(food[0], food[1], '*') 
        # Get user input
        new_key = win.getch()
        key = key if new_key == -1 else new_key  

        head = snake[0][:]
        if key == curses.KEY_UP:
            head[0] -= 1
        elif key == curses.KEY_DOWN:
            head[0] += 1
        elif key == curses.KEY_LEFT:
            head[1] -= 1
        elif key == curses.KEY_RIGHT:
            head[1] += 1

        if head in snake or head[0] in [0, 19] or head[1] in [0, 59]:
            break


        snake.insert(0, head)


        if head == food:
            food = [random.randint(1, 18), random.randint(1, 58)] 
            win.addch(food[0], food[1], '*')
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')  

        win.addch(snake[0][0], snake[0][1], '#')  
        win.timeout(100)  


    curses.endwin()
    print("Game Over!")

if __name__ == "__main__":
    snake_game()
