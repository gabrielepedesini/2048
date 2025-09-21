import threading
import random
import time
import curses

board = None
not_addable = None
score = None
game_over = None
move_lock = threading.Lock()
colors = {
    2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7, 256: 8, 512: 9, 1024: 10, 2048: 11
}


# =============================
# Initializes game
# =============================

def init_game():
    global board, not_addable, score, game_over
    
    board = [   
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]

    not_addable = [
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False]
    ]

    score = 0
    game_over = False

    generate_tile()
    generate_tile()


# =============================
# Resets not addable matrix
# =============================

def reset_not_addable():
    for i in range(0, len(not_addable)):
        for j in range(0, len(not_addable[0])):
            not_addable[i][j] = False


# =============================
# Moves tile in a empty space
# =============================

def move_tile(start: list[int], end: list[int]):
    temp = board[start[0]][start[1]]
    board[end[0]][end[1]] = temp
    board[start[0]][start[1]] = None


# =============================
# Sums tiles
# =============================

def sum_tiles(start: list[int], end: list[int]):
    global score
    board[end[0]][end[1]] *= 2
    board[start[0]][start[1]] = None
    not_addable[end[0]][end[1]] = True
    score += board[end[0]][end[1]]


# =============================
# Generates new tile
# =============================

def generate_tile():
    value = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
    position = random.randint(0, 64)
    row = 0
    col = 0 
    
    while position > 0 or board[row][col] != None:
        if col < len(board[0]) - 1:
            col += 1
        elif row < len(board) - 1:
            row += 1
            col = 0
        else:
            row = 0
            col = 0

        if board[row][col] == None:
            position -= 1
    
    board[row][col] = value


# =============================
# Checks game over
# =============================

def check_game_over():
    global game_over

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == None:
                return
            
            if j < len(board[0]) - 1 and board[i][j] == board[i][j + 1]:
                return
            
            if i < len(board) - 1 and board[i][j] == board[i + 1][j]:
                return 

    game_over = True
    return


# =============================
# Moves left
# =============================

def move_left():
    if not move_lock.acquire(blocking=False):
        return
    
    changes = 0

    for i in range(0, len(board)):
        for j in range(1, len(board[0])):
            if board[i][j] == None:
                continue
            
            for k in range(j, 0, -1):
                if board[i][k - 1] == None:
                    move_tile([i, k], [i, k - 1])
                    changes += 1
                elif board[i][k] == board[i][k - 1] and board[i][k] < 2048 and not not_addable[i][k - 1] and not not_addable[i][k]:
                    sum_tiles([i, k], [i, k - 1])
                    changes += 1
                else:
                    break
            
    if changes > 0:
        generate_tile()
        reset_not_addable()

    check_game_over()

    move_lock.release()


# =============================
# Moves right
# =============================

def move_right():
    if not move_lock.acquire(blocking=False):
        return
    
    changes = 0

    for i in range(0, len(board)):
        for j in range(len(board[0]) - 2, -1, -1):
            if board[i][j] == None:
                continue
            
            for k in range(j, len(board[0]) - 1):
                if board[i][k + 1] == None:
                    move_tile([i, k], [i, k + 1])
                    changes += 1
                elif board[i][k] == board[i][k + 1] and board[i][k] < 2048 and not not_addable[i][k + 1] and not not_addable[i][k]:
                    sum_tiles([i, k], [i, k + 1])
                    changes += 1
                else:
                    break
            
    if changes > 0:
        generate_tile()
        reset_not_addable()

    check_game_over()

    move_lock.release()


# =============================
# Moves up
# =============================

def move_up():
    if not move_lock.acquire(blocking=False):
        return

    changes = 0

    for j in range(0, len(board[0])):
        for i in range(1, len(board)):
            if board[i][j] == None:
                continue
            
            for k in range(i, 0, -1):
                if board[k - 1][j] == None:
                    move_tile([k, j], [k - 1, j])
                    changes += 1
                elif board[k][j] == board[k - 1][j] and board[k][j] < 2048 and not not_addable[k - 1][j] and not not_addable[k][j]:
                    sum_tiles([k, j], [k - 1, j])
                    changes += 1
                else:
                    break
            
    if changes > 0:
        generate_tile()
        reset_not_addable()

    check_game_over()

    move_lock.release()


# =============================
# Moves down
# =============================

def move_down():
    if not move_lock.acquire(blocking=False):
        return
    
    changes = 0

    for j in range(0, len(board[0])):
        for i in range(len(board) - 2, -1, -1):
            if board[i][j] == None:
                continue
            
            for k in range(i, len(board) - 1):
                if board[k + 1][j] == None:
                    move_tile([k, j], [k + 1, j])
                    changes += 1
                elif board[k][j] == board[k + 1][j] and board[k][j] < 2048 and not not_addable[k + 1][j] and not not_addable[k][j]:
                    sum_tiles([k, j], [k + 1, j])
                    changes += 1
                else:
                    break
            
    if changes > 0:
        generate_tile()
        reset_not_addable()

    check_game_over()

    move_lock.release()
        

# =============================
# Draws board
# =============================

def draw_board(stdscr):
    stdscr.clear()
    width = 4

    cols = len(board[0])
    rows = len(board)

    tl = "┌" 
    tr = "┐"  
    bl = "└"  
    br = "┘"  
    hor = "─"  
    ver = "│" 
    top_sep = "┬"
    bottom_sep = "┴"
    left_sep = "├"
    right_sep = "┤"
    center_sep = "┼"

    top_line = tl
    for c in range(cols):
        top_line += hor * width
        if c < cols-1:
            top_line += top_sep
    top_line += tr + "\n"
    stdscr.addstr(top_line)

    for r, row in enumerate(board):
        row_str = ver
        for x in row:
            stdscr.addstr(ver, curses.color_pair(0))

            if x is None:
                cell = " " * width
                stdscr.addstr(cell, curses.color_pair(0))
            else:
                color_pair = colors.get(x, 0)
                cell = str(x).center(width)
                stdscr.addstr(cell, curses.color_pair(color_pair))
        stdscr.addstr(ver + "\n", curses.color_pair(0))

        if r < rows - 1:
            sep_line = left_sep
            for c in range(cols):
                sep_line += hor * width
                if c < cols - 1:
                    sep_line += center_sep
            sep_line += right_sep + "\n"
            stdscr.addstr(sep_line)

    bottom_line = bl
    for c in range(cols):
        bottom_line += hor * width
        if c < cols - 1:
            bottom_line += bottom_sep
    bottom_line += br + "\n"
    stdscr.addstr(bottom_line)

    if game_over:
        stdscr.addstr("\nGame Over! No more moves possible...\n")

    stdscr.addstr(f"\nScore: {score}\n")
    stdscr.addstr("\n'wasd' or arrow buttons - move")
    stdscr.addstr("\n'r' - restart")
    stdscr.addstr("\n'q' - quit\n")
    
    stdscr.refresh()


# =============================
# Main game loop
# =============================

def game_loop(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)    
    stdscr.keypad(True)   

    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, 15, -1)    # 2 → white
    curses.init_pair(2, 190, -1)   # 4 → light yellow
    curses.init_pair(3, 82, -1)    # 8 → bright green
    curses.init_pair(4, 155, -1)   # 16 → green
    curses.init_pair(5, 39, -1)    # 32 → blue
    curses.init_pair(6, 201, -1)   # 64 → magenta
    curses.init_pair(7, 208, -1)   # 128 → orange
    curses.init_pair(8, 220, -1)   # 256 → golden yellow
    curses.init_pair(9, 93, -1)    # 512 → purple
    curses.init_pair(10, 33, -1)   # 1024 → teal
    curses.init_pair(11, 196, -1)  # 2048 → bright red

    while True:
        draw_board(stdscr)
        key = stdscr.getch()

        if key in (ord('q'), ord('Q')):
            break
        elif key in (ord('r'), ord('R')):
            init_game()
        elif key in (ord('w'), ord('W'), curses.KEY_UP, 450):
            move_up()
        elif key in (ord('a'), ord('A'), curses.KEY_LEFT, 452):
            move_left()
        elif key in (ord('d'), ord('D'), curses.KEY_RIGHT, 454):
            move_right()
        elif key in (ord('s'), ord('S'), curses.KEY_DOWN, 456):
            move_down()

        time.sleep(0.05)


if __name__ == "__main__":
    init_game()
    curses.wrapper(game_loop)