import numpy as np
import matplotlib.pyplot as plt

def get_neighborhood(i,j, i_shape, j_shape):
    nbs =  [(i-1, j), (i-1, j-1), (i, j-1),
            (i+1, j-1), (i-1, j+1), (i+1, j),
            (i+1, j+1), (i, j+1)]
    # Wrap around
    nbs = [(v[0]%i_shape, v[1]%j_shape) for v in nbs]
    return nbs

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
    i_shape = board_shape[0]
    j_shape = board_shape[1]

    for i in range(board_shape[0] - 1):
        for j in range(board_shape[1] - 1):
            nb_cells = 0
            nbs = get_neighborhood(i,j, i_shape, j_shape)
            for nb in nbs:
                nb_cells += board[nb[0], nb[1]]

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
