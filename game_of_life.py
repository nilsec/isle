import numpy as np
import matplotlib.pyplot as plt

def step(board):
    """
    Implements one evolution step of the game of life.
    Rules:

    1. Any live cell with two or three live neighbours survives.
    2. Any dead cell with three live neighbours becomes a live cell.
    3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.
    """

    board_shape = np.shape(board)
    board_new = np.zeros(board_shape, dtype=np.bool)

    for i in range(board_shape[0] - 1):
        for j in range(board_shape[1] - 1):
            nb_cells = 0

            nb_cells += board[i - 1][j - 1] #top left
            nb_cells += board[i - 1][j]  #top center
            nb_cells += board[i - 1][j + 1] #top right

            nb_cells += board[i][j - 1] #middle left
            nb_cells += board[i][j + 1] #middle right

            nb_cells += board[i + 1][j - 1] #bottom left
            nb_cells += board[i + 1][j] #bottom center
            nb_cells += board[i + 1][j + 1] #bottom right

            if nb_cells == 2: # Dead cells stay dead, live cells survive
                board_new[i,j] = board[i,j]
            elif nb_cells == 3: # Live cells stay alive, dead cells become alive:
                board_new[i,j] = 1
            else:
                board_new[i,j] = 0

    return board_new

def init_random(height, width):
    board = np.random.rand(height, width) > 0.5
    return board

def show_sequence(im_sequence):
    curr_pos = 0
    def key_event(e):
        nonlocal curr_pos
        if e.key == "right":
            curr_pos = curr_pos + 1
        elif e.key == "left":
            curr_pos = curr_pos - 1
        else:
            return
        curr_pos = curr_pos % len(im_sequence)

        ax.cla()
        ax.imshow(im_sequence[curr_pos])
        fig.canvas.draw()

    fig = plt.figure()
    fig.canvas.mpl_connect('key_press_event', key_event)
    ax = fig.add_subplot(111)
    ax.imshow(im_sequence[0])
    plt.show()

if __name__ == "__main__":
    t0 = init_random(10,10)
    t1 = step(t0)

    show_sequence([t0, t1])
