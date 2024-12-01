import tkinter as tk
from tkinter import messagebox
import random
import math


class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TicTacToe-Trung Phương")
        self.window.iconbitmap('icon.ico')
        self.center_window(500, 500)
        self.window.configure(bg="#7ebaf3")
        self.current_player = "X"
        self.board_size = 3
        self.win_condition = 3
        self.buttons = []
        self.game_mode = None  # 'PvP', 'PvC', 'CvC'
        self.winning_cells = []  # Danh sách các ô thắng cuộc
        self.algorithm_p1 = None  # Thuật toán của máy 1
        self.algorithm_p2 = None  # Thuật toán của máy 2
        self.show_game_type_selection()

    def center_window(self, width, height):
        """Đặt cửa sổ ở giữa màn hình."""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def show_game_type_selection(self):
        """Hiển thị lựa chọn kiểu chơi."""
        tk.Frame(self.window).pack(pady=20)
        label = tk.Label(self.window, text="Chọn kiểu chơi: ", font=("Arial", 25))
        label.pack(pady=10)

        btn_pvp = tk.Button(
            self.window, text="Player vs Player", font=("Arial", 14),
            width=20, height=1, 
            bg="lightblue",  # Màu nền
            activebackground="lightgreen",  # Màu khi nhấn
            fg="darkblue",
            command=lambda: self.select_game_mode("PvP")
        )
        btn_pvp.pack(pady=5)

        btn_pvc = tk.Button(
            self.window, text="Player vs Computer", font=("Arial", 14),
            width=20, height=1, 
            bg="lightblue",  # Màu nền
            activebackground="lightgreen",  # Màu khi nhấn
            fg="darkblue",
            command=lambda: self.select_game_mode("PvC")
        )
        btn_pvc.pack(pady=5)

        btn_cvc = tk.Button(
            self.window, text="Computer vs Computer", font=("Arial", 14),
            width=20, height=1, 
            bg="lightblue",  # Màu nền
            activebackground="lightgreen",  # Màu khi nhấn
            fg="darkblue",
            command=lambda: self.select_game_mode("CvC")
        )
        btn_cvc.pack(pady=5)

        game_name_label = tk.Label(
        self.window, 
        text="Trình Quang Trung_22110256\nLê Duy Phương_22110205.", 
        font=("Arial", 10), 
        bg="#7ebaf3", 
        fg="darkblue"
        )
        game_name_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        

    def select_game_mode(self, mode):
        """Lưu kiểu chơi và chuyển sang giao diện chọn thuật toán nếu cần."""
        self.game_mode = mode
        if mode == "PvP":
            self.show_mode_selection()
        elif mode == "PvC":
            self.show_algorithm_selection(player="Computer", next_action=self.show_mode_selection)
        elif mode == "CvC":
            self.show_algorithm_selection(player="Computer 1", next_action=lambda: self.show_algorithm_selection(
                player="Computer 2", next_action=self.show_mode_selection))

    def show_algorithm_selection(self, player, next_action):
        """Hiển thị lựa chọn thuật toán cho người chơi hoặc máy."""
        for widget in self.window.winfo_children():
            widget.destroy()

        # Tạo một frame chứa các nút
        tk.Frame(self.window).pack(pady=20)

        label = tk.Label(self.window, text=f"Chọn thuật toán cho {player}:", font=("Arial", 20))
        label.pack(pady=10)

        # Tạo một frame chứa các nút
        tk.Frame(self.window).pack(pady=5)

        algorithms = ["Minimax", "DFS", "A-Star", "Backtracking", "Simulated Annealing", "Hill Climbing"]

        for algo in algorithms:
            btn = tk.Button(
                self.window, 
                text=algo, 
                font=("Arial", 14),
                width=20, height=1,
                bg="lightblue",  # Màu nền
                activebackground="lightgreen",  # Màu khi nhấn
                fg="darkblue",  # Màu chữ
                command=lambda algo=algo: self.select_algorithm(player, algo, next_action)
            )
            btn.pack(pady=5)
        
        game_name_label = tk.Label(
        self.window, 
        text="Trình Quang Trung_22110256\nLê Duy Phương_22110205.", 
        font=("Arial", 10), 
        bg="#7ebaf3", 
        fg="darkblue"
        )
        game_name_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        

    def select_algorithm(self, player, algorithm, next_action):
        """Ghi nhận thuật toán được chọn và thực hiện bước tiếp theo."""
        if player == "Computer":
            self.algorithm_p2 = algorithm
        elif player == "Computer 1":
            self.algorithm_p1 = algorithm
        elif player == "Computer 2":
            self.algorithm_p2 = algorithm

        next_action()

    def show_mode_selection(self):
        """Hiển thị màn hình chọn chế độ."""
        for widget in self.window.winfo_children():
            widget.destroy()

        tk.Frame(self.window).pack(pady=20)
        label = tk.Label(self.window, text="Chọn chế độ chơi:", font=("Arial", 20))
        label.pack(pady=10)

        for size, win_condition in [(3, 3), (6, 4), (9, 5), (11, 6)]:
            btn = tk.Button(
                self.window, text=f"{size}x{size} (Thắng {win_condition} ô)",
                font=("Arial", 14),
                width=20, height=1, 
                bg="lightblue",  # Màu nền
                activebackground="lightgreen",  # Màu khi nhấn
                fg="darkblue",
                command=lambda s=size, w=win_condition: self.start_game(s, w)
            )
            btn.pack(pady=5)

        game_name_label = tk.Label(
        self.window, 
        text="Trình Quang Trung_22110256\nLê Duy Phương_22110205.", 
        font=("Arial", 10), 
        bg="#7ebaf3", 
        fg="darkblue"
        )
        game_name_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def start_game(self, board_size, win_condition):
        """Khởi động trò chơi với kích thước bảng và điều kiện thắng."""
        self.board_size = board_size
        self.win_condition = win_condition
        self.current_player = "X"
        self.winning_cells = []  # Reset danh sách các ô thắng cuộc

        # Dọn dẹp giao diện hiện tại
        for widget in self.window.winfo_children():
            widget.destroy()

        # Tính toán kích thước cửa sổ dựa trên kích thước bảng
        cell_size = 100  # Kích thước mỗi ô
        window_size = cell_size * board_size
        self.center_window(window_size + 200, window_size + 200)  # Thêm không gian để căn giữa

        # Tạo frame trung tâm
        center_frame = tk.Frame(self.window, bg="#7ebaf3")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Hiển thị nhãn lượt chơi
        self.label = tk.Label(center_frame, text=f"Lượt chơi: {self.current_player}", 
                            font=("Arial", 20), bg="#7ebaf3")
        self.label.pack(pady=10)

        # Tạo bảng chơi
        board_frame = tk.Frame(center_frame, bg="#7ebaf3")
        board_frame.pack()

        self.buttons = [[None for _ in range(board_size)] for _ in range(board_size)]
        
        # Tạo bảng chơi
        for i in range(board_size):
            for j in range(board_size):
                button = tk.Button(
                    board_frame, 
                    text="", 
                    font=("Arial", 16),
                    width=7, 
                    height=3,
                    bg="lightblue",
                    activebackground="lightgreen",  # Màu khi nhấn
                    fg="darkblue", 
                    command=lambda row=i, col=j: self.on_click(row, col)
                )
                button.grid(row=i, column=j, padx=2, pady=2)
                self.buttons[i][j] = button

        game_name_label = tk.Label(
        self.window, 
        text="Trình Quang Trung_22110256\nLê Duy Phương_22110205.", 
        font=("Arial", 10), 
        bg="#7ebaf3", 
        fg="darkblue"
        )
        game_name_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        # Nếu chế độ là CvC, tự động chạy
        if self.game_mode == "CvC":
            self.window.after(1000, self.computer_vs_computer_turn)

    def create_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                button = tk.Button(
                    self.window, 
                    text="", 
                    font=("Arial", 16),
                    width=7, 
                    height=3,
                    bg="lightblue",
                    activebackground="lightgreen",  # Màu khi nhấn
                    fg="darkblue", 
                    command=lambda row=i, col=j: self.on_click(row, col)
                )

                button.grid(row=i + 1, column=j, sticky="nsew")  
                self.buttons[i][j] = button

    def on_click(self, row, col):
        if (self.game_mode in ["PvC", "CvC"] and self.current_player == "O"):
            return

        if self.buttons[row][col]["text"] == "":
            self.buttons[row][col]["text"] = self.current_player
            if self.check_winner(row, col):
                self.highlight_winner()
                messagebox.showinfo("Game Over", f"Người chơi {self.current_player} thắng!")
                self.reset_board()
                return
            elif self.is_draw():
                messagebox.showinfo("Game Over", "Hòa!")
                self.reset_board()
                return

            self.current_player = "O" if self.current_player == "X" else "X"
            self.update_label()

            if self.game_mode == "PvC" and self.current_player == "O":
                self.disable_board()  # Vô hiệu hóa bàn cờ khi máy tính đang chơi
                self.window.after(500, self.computer_turn)

    def disable_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].config(state="disabled")

    def enable_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].config(state="normal")

    def computer_turn(self):
        """Máy tính thực hiện lượt chơi."""
        move = None
        if self.algorithm_p2 == "Minimax":
            move = self.find_best_move()
        elif self.algorithm_p2 == "DFS":
            move = self.dfs_move()
        elif self.algorithm_p2 == "A-Star":
            move = self.a_star_move()
        elif self.algorithm_p2 == "Backtracking":
            move = self.backtracking_move()
        elif self.algorithm_p2 == "Simulated Annealing":
            move = self.simulated_annealing_move()
        elif self.algorithm_p2 == "Hill Climbing":
            move = self.hill_climbing_move()

        if move:
            row, col = move
            self.buttons[row][col]["text"] = self.current_player
            if self.check_winner(row, col):
                self.highlight_winner()
                messagebox.showinfo("Game Over", f"Người chơi {self.current_player} thắng!")
                self.reset_board()
                return
            elif self.is_draw():
                messagebox.showinfo("Game Over", "Hòa!")
                self.reset_board()
                return

            self.current_player = "X"
            self.update_label()
            self.enable_board()

    def a_star_move(self):
        """Tìm nước đi tốt nhất bằng thuật toán A*."""
        board = [[self.buttons[i][j]["text"] for j in range(self.board_size)] for i in range(self.board_size)]

        def heuristic(board, player):
            """Tính giá trị heuristic dựa trên số lượng các ô có lợi cho người chơi."""
            opponent = "X" if player == "O" else "O"
            score = 0
            for i in range(self.board_size):
                row = [board[i][j] for j in range(self.board_size)]
                col = [board[j][i] for j in range(self.board_size)]
                score += row.count(player) - row.count(opponent)
                score += col.count(player) - col.count(opponent)

            diag1 = [board[i][i] for i in range(self.board_size)]
            diag2 = [board[i][self.board_size - 1 - i] for i in range(self.board_size)]
            score += diag1.count(player) - diag1.count(opponent)
            score += diag2.count(player) - diag2.count(opponent)
            return score

        best_move = None
        best_score = -float("inf")

        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = heuristic(board, "O")
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
                    board[i][j] = ""
        return best_move
    
    def dfs_move(self):
        """Tìm nước đi tốt nhất bằng thuật toán DFS."""
        def dfs(board, player, depth):
            """Hàm đệ quy DFS để kiểm tra các trạng thái bảng."""
            # Kiểm tra điều kiện kết thúc
            if self.check_full_win("X"):
                return -10 + depth  # Người chơi "X" thắng
            if self.check_full_win("O"):
                return 10 - depth  # Người chơi "O" thắng
            if self.is_draw():
                return 0  # Hòa

            # Duyệt qua tất cả các nước đi có thể
            scores = []
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if board[i][j] == "":
                        board[i][j] = player  # Thử nước đi
                        score = dfs(
                            board, "O" if player == "X" else "X", depth + 1
                        )  # Chuyển lượt
                        scores.append(score)
                        board[i][j] = ""  # Hoàn tác nước đi

            # Trả về điểm tối đa/tối thiểu
            if not scores:  # Nếu không có nước đi hợp lệ
                return 0  # Hòa
            return max(scores) if player == "O" else min(scores)

        # Khởi tạo trạng thái bảng
        board = [[self.buttons[i][j]["text"] for j in range(self.board_size)] for i in range(self.board_size)]
        best_score = -float("inf")
        best_move = None

        # Thử từng ô trống để tìm nước đi tốt nhất
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = dfs(board, "X", 0)
                    board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        return best_move

    def minimax(self, is_maximizing, depth=0):
        """Cài đặt thuật toán Minimax."""
        if self.check_full_win("X"):
            return -10 + depth
        if self.check_full_win("O"):
            return 10 - depth
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = "O"
                        score = self.minimax(False, depth + 1)
                        self.buttons[i][j]["text"] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = "X"
                        score = self.minimax(True, depth + 1)
                        self.buttons[i][j]["text"] = ""
                        best_score = min(score, best_score)
            return best_score

    def find_best_move(self):
        """Tìm nước đi tốt nhất cho máy."""
        best_score = -float("inf")
        move = None
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.buttons[i][j]["text"] == "":
                    self.buttons[i][j]["text"] = "O"
                    score = self.minimax(False)
                    self.buttons[i][j]["text"] = ""
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move

    def backtracking_move(self):
        """Tìm nước đi tốt nhất bằng thuật toán Backtracking."""
        def can_win(board, player, depth=0):
            """Kiểm tra xem nước đi có thể dẫn đến chiến thắng không."""
            if self.check_full_win(player):
                return True
            if self.is_draw():
                return False

            for i in range(self.board_size):
                for j in range(self.board_size):
                    if board[i][j] == "":
                        board[i][j] = player
                        if not can_win(board, "X" if player == "O" else "O", depth + 1):
                            board[i][j] = ""
                            return True
                        board[i][j] = ""
            return False

        board = [[self.buttons[i][j]["text"] for j in range(self.board_size)] for i in range(self.board_size)]
        best_move = None

        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == "":
                    board[i][j] = "O"
                    if can_win(board, "O"):
                        best_move = (i, j)
                        board[i][j] = ""
                        break
                    board[i][j] = ""
            if best_move:
                break

        # Nếu không tìm thấy nước đi tốt nhất, chọn nước đi ngẫu nhiên
        if not best_move:
            empty_cells = [(i, j) for i in range(self.board_size) for j in range(self.board_size) if board[i][j] == ""]
            if empty_cells:
                best_move = random.choice(empty_cells)

        return best_move


    def hill_climbing_move(self):
        """Tìm nước đi tốt nhất bằng thuật toán Hill Climbing."""
        board = [[self.buttons[i][j]["text"] for j in range(self.board_size)] for i in range(self.board_size)]

        def heuristic(board, player):
            """Tính giá trị heuristic dựa trên số lượng các ô có lợi cho người chơi."""
            opponent = "X" if player == "O" else "O"
            score = 0
            for i in range(self.board_size):
                row = [board[i][j] for j in range(self.board_size)]
                col = [board[j][i] for j in range(self.board_size)]
                score += row.count(player) - row.count(opponent)
                score += col.count(player) - col.count(opponent)

            diag1 = [board[i][i] for i in range(self.board_size)]
            diag2 = [board[i][self.board_size - 1 - i] for i in range(self.board_size)]
            score += diag1.count(player) - diag1.count(opponent)
            score += diag2.count(player) - diag2.count(opponent)
            return score

        best_move = None
        current_score = -float("inf")

        # Khởi tạo các trạng thái nước đi hợp lệ
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == "":
                    board[i][j] = "O"  # Giả lập nước đi
                    score = heuristic(board, "O")
                    board[i][j] = ""  # Hoàn tác nước đi

                    # Nếu tìm được điểm tốt hơn, cập nhật nước đi
                    if score > current_score:
                        current_score = score
                        best_move = (i, j)

        return best_move

    def simulated_annealing_move(self):
        """Tìm nước đi tốt nhất bằng thuật toán Simulated Annealing."""
        board = [[self.buttons[i][j]["text"] for j in range(self.board_size)] for i in range(self.board_size)]

        def heuristic(board, player):
            """Tính điểm heuristic đơn giản: số ô có lợi thế."""
            opponent = "X" if player == "O" else "O"
            player_score = sum(row.count(player) for row in board)
            opponent_score = sum(row.count(opponent) for row in board)
            return player_score - opponent_score

        def get_neighbors(board):
            """Lấy danh sách các nước đi hợp lệ."""
            return [(i, j) for i in range(self.board_size) for j in range(self.board_size) if board[i][j] == ""]

        temperature = 100  # Nhiệt độ ban đầu
        cooling_rate = 0.95  # Tỉ lệ giảm nhiệt độ
        current_state = random.choice(get_neighbors(board))  # Chọn một nước đi ban đầu
        current_score = -float("inf")

        while temperature > 1:
            # Lấy một trạng thái hàng xóm ngẫu nhiên
            neighbors = get_neighbors(board)
            if not neighbors:
                break
            next_state = random.choice(neighbors)

            # Giả lập nước đi
            board[next_state[0]][next_state[1]] = "O"
            next_score = heuristic(board, "O")
            board[next_state[0]][next_state[1]] = ""  # Hoàn tác

            # Quyết định chấp nhận trạng thái mới
            if next_score > current_score or math.exp((next_score - current_score) / temperature) > random.random():
                current_state, current_score = next_state, next_score

            # Giảm nhiệt độ
            temperature *= cooling_rate

        return current_state

    def check_full_win(self, player):
        """Kiểm tra nếu người chơi thắng."""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.buttons[i][j]["text"] == player:
                    for dr, dc in directions:
                        count = 0
                        for step in range(self.win_condition):
                            r, c = i + dr * step, j + dc * step
                            if 0 <= r < self.board_size and 0 <= c < self.board_size and self.buttons[r][c]["text"] == player:
                                count += 1
                            else:
                                break
                        if count >= self.win_condition:
                            return True
        return False

    def check_winner(self, row, col):
        """Kiểm tra thắng cuộc."""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        player = self.buttons[row][col]["text"]
        for dr, dc in directions:
            count = 0
            self.winning_cells = []
            for step in range(-self.win_condition + 1, self.win_condition):
                r, c = row + dr * step, col + dc * step
                if 0 <= r < self.board_size and 0 <= c < self.board_size and self.buttons[r][c]["text"] == player:
                    count += 1
                    self.winning_cells.append((r, c))
                    if count == self.win_condition:
                        return True
                else:
                    count = 0
                    self.winning_cells = []
        return False

    def is_draw(self):
        """Kiểm tra nếu hòa."""
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.buttons[i][j]["text"] == "":
                    return False
        return True

    def update_label(self):
        """Cập nhật nhãn lượt chơi."""
        self.label.config(text=f"Lượt chơi: {self.current_player}")

    def highlight_winner(self):
        """Làm nổi bật ô thắng cuộc."""
        for r, c in self.winning_cells:
            self.buttons[r][c].config(bg="lightgreen")

    def reset_board(self):
        """Đặt lại trò chơi."""
        for widget in self.window.winfo_children():
            widget.destroy()
        self.show_game_type_selection()

    def computer_vs_computer_turn(self):
        if self.game_mode != "CvC":
            return

        algorithm = self.algorithm_p1 if self.current_player == "X" else self.algorithm_p2
        move = None
        if algorithm == "Minimax":
            move = self.find_best_move()
        elif algorithm == "DFS":
            move = self.dfs_move()
        elif algorithm == "A-Star":
            move = self.a_star_move()
        elif algorithm == "Backtracking":
            move = self.backtracking_move()
        elif algorithm == "Simulated Annealing":
            move = self.simulated_annealing_move()
        elif algorithm == "Hill Climbing":
            move = self.hill_climbing_move()

        if not move:
            messagebox.showinfo("Game Over", "Không có nước đi hợp lệ!")
            self.reset_board()
            return

        row, col = move
        self.buttons[row][col]["text"] = self.current_player
        if self.check_winner(row, col):
            self.highlight_winner()
            messagebox.showinfo("Game Over", f"Người chơi {self.current_player} thắng!")
            self.reset_board()
            return
        elif self.is_draw():
            messagebox.showinfo("Game Over", "Hòa!")
            self.reset_board()
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_label()
        self.window.after(500, self.computer_vs_computer_turn)

# Chạy trò chơi
if __name__ == "__main__":
    game = TicTacToe()
    game.window.mainloop()  