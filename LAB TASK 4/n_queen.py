def is_safe(board, row, col, n):
    for i in range(col):
        if board[row][i] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    return True
def solve_n_queens_util(board, col, n):
    if col >= n:
        return True
    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1
            if solve_n_queens_util(board, col + 1, n):
                return True
            board[i][col] = 0
    return False
def solve_n_queens(n):
    board = [[0] * n for _ in range(n)]
    if not solve_n_queens_util(board, 0, n):
        return None
    return board
def print_board(board):
    for row in board:
        print(" ".join("Q" if cell else "." for cell in row))
def main():
    while True:
        try:
            n = int(input("Enter the value of N: "))
            if n < 1:
                print("Invalid number! Please enter a positive integer.")
                continue
            if n in [1, 2, 3]:
                print("Solution is not possible for N =", n)
            else:
                result = solve_n_queens(n)
                if result is None:
                    print("Solution does not exist!")
                else:
                    print("Here is a possible solution:")
                    print_board(result)
        except ValueError:
            print("Invalid input! Please enter a valid integer.")
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print("Thanks for playing!")
            break
if __name__ == "__main__":
    main()