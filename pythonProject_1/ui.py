from tkinter import Tk, Frame, Button, LEFT, RIGHT, NORMAL, BOTH, DISABLED, Spinbox
import tkinter as tk  # For StringVar
from tkinter import ttk  # For dropdown



# Assuming you have these classes in separate files
# For instance, create a stub Board class in each of these files

# class Board:
#     def __init__(self, ply=1):
#         self.ply = ply
#         self.board = [[['-' for _ in range(4)] for _ in range(4)] for _ in range(4)]
#         # Add other necessary attributes and methods as per your implementation


class TTTBtn(Button):
    def __init__(self, master=None, pos=None, **kwargs):
        Button.__init__(self, master, **kwargs)
        self.pos = pos


class TTTUI(object):
    default_ply = 1
    neither_color = '#%02x%02x%02x' % (255, 255, 255)  # white
    player_color = '#%02x%02x%02x' % (62, 188, 0)  # green
    computer_color = '#%02x%02x%02x' % (192, 35, 3)  # red
    win_color = '#%02x%02x%02x' % (25, 111, 254)  # blue

    def __init__(self):
        # TTT related
        # Initialize with a default Board instance
        from heuristic_with_alphabita import Board
        self.ttt = Board(ply=1)  # This assumes you have a default Board instance defined
        self.human_first = True

        # UI related
        self.root = Tk()
        self.root.resizable(0, 0)
        self.root.title("3D TTT")

        # TTT frames
        self.ttt_frames = [Frame(self.root) for x in range(4)]
        for i in range(4):
            self.ttt_frames[i].grid(row=0, column=i)
        self.button_pos = dict()
        self._init_board()

        # File selection frame
        self.file_frame = Frame(self.root, padx=5, pady=5)
        self.file_frame.grid(row=1, column=0, columnspan=4)

        # Dropdown for file selection
        self.selected_file = tk.StringVar()
        files = ['heuristic with alphabeta', 'heuristic with minimax']
        self.file_dropdown = ttk.Combobox(self.file_frame, textvariable=self.selected_file, values=files)
        self.file_dropdown.current(0)  # Set default selection
        self.selected_file.set(files[0])  # Ensure the default value is set
        self.file_dropdown.pack(side=LEFT)

        # Button to confirm file selection
        self.select_file_btn = Button(self.file_frame, text='Select File', command=self.import_board)
        self.select_file_btn.pack(side=LEFT)

        # control frame
        self.control_frame = Frame(self.root, padx=5, pady=5)
        self.control_frame.grid(row=2, column=1, columnspan=2)
        self.new_game_btn = Button(self.control_frame, text='New Game', command=lambda: self.reset())
        self.new_game_btn.pack(side=LEFT, fill=BOTH, expand=True)
        self.toggle_human_first_btn = Button(self.control_frame, text='Human First',
                                             command=lambda: self.toggle_human_first())
        self.toggle_human_first_btn.pack(side=RIGHT, fill=BOTH, expand=True)
        self.ply_box = Spinbox(self.control_frame, from_=1, to=20, textvariable=self.ttt.difficulty,
                               command=lambda: self.reset())
        self.ply_box.pack(side=RIGHT, fill=BOTH, expand=True)

        # start UI
        self.update_pieces()
        self.start()
        self.root.mainloop()

    def toggle_human_first(self):
        self.human_first = not self.human_first
        self.toggle_human_first_btn.config(text='Human First' if \
            self.human_first else 'Computer First')
        self.reset()

    def _find_button(self, frame, r, c):
        for child in list(frame.children.values()):
            info = child.grid_info()
            if info['row'] == r and info['column'] == c:
                return child
        return None

    def update_pieces(self):
        player_pieces = self.ttt.get_moves(self.ttt.human)
        computer_pieces = self.ttt.get_moves(self.ttt.ai)

        cnt = 0
        for b, board in enumerate(self.ttt.board):
            for r, row in enumerate(board):
                for c, col in enumerate(row):
                    color = self.neither_color
                    text = '-'
                    occupied = False
                    if cnt in player_pieces:
                        color = self.player_color
                        text = self.ttt.human
                    if cnt in computer_pieces:
                        color = self.computer_color
                        text = self.ttt.ai
                    if self.ttt.complete and cnt in self.ttt.winning_combo:
                        color = self.win_color
                    btn = self.button_pos[cnt]
                    btn.config(text=text, bg=color, state=DISABLED if \
                        occupied else NORMAL)
                    cnt += 1

    def place_human(self, position):
        if position in self.ttt.allowed_moves and not self.ttt.complete:
            self.ttt.move(position, self.ttt.human)
            self.ttt.human_turn = False
            self.update_pieces()
            self.place_computer()

    def place_computer(self):
        if not self.ttt.complete:
            self.ttt.computers_move()
            self.update_pieces()

    def reset(self):
        self.ttt.reset()
        self.ttt.difficulty = self.default_ply if not \
            self.ply_box.get().isdigit() else int(self.ply_box.get())
        self.ttt.human_turn = self.human_first
        self.update_pieces()
        self.start()

    def _init_board(self):
        cnt = 0
        for b, board in enumerate(self.ttt.board):
            for x, row in enumerate(board):
                for y, cell in enumerate(row):
                    padding = (0, 0)
                    if y == 3 and b != 3:
                        padding = (0, 12)
                    btn = Button(self.ttt_frames[b], width=8, height=4, command=lambda x=cell: self.place_human(x))
                    btn.grid(row=x, column=y, padx=padding)
                    self.button_pos[cnt] = btn
                    cnt += 1

    def start(self):
        if not self.ttt.human_turn:
            self.place_computer()

    def import_board(self):
        selected_option = self.selected_file.get()
        if selected_option == 'heuristic with alphabeta':
            from heuristic_with_alphabita import Board
        elif selected_option == 'heuristic with minimax':
            from heuristic_with_minimax import Board
        else:
            print("Invalid selection")  # Add appropriate error handling

        # Use the selected Board class for further operations
        self.ttt = Board(ply=1)  # For instance, initializing with selected Board class
        self.reset()  # Reset the game with the newly selected Board
        self._init_board()  # Call this method again after initializing self.ttt


if __name__ == '__main__':
    t = TTTUI()
