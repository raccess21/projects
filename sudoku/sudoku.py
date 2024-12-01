import os

boardo = [
	[3, 9, 5, 7, 8, 1, 2, 4, 6],
	[7, 8, 0, 0, 0, 0, 5, 9, 0],
	[4, 0, 6, 5, 0, 0, 8, 0, 7],
	[2, 0, 3, 0, 0, 0, 0, 1, 0],
	[8, 0, 0, 4, 7, 3, 0, 0, 0],
	[9, 6, 0, 0, 0, 0, 3, 0, 4],
	[5, 0, 9, 0, 0, 7, 1, 0, 0],
	[6, 7, 8, 0, 0, 0, 0, 2, 0],
	[1, 0, 0, 0, 2, 0, 0, 0, 9],
]

#output sudoku board
def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]), end=" ")
    print("____________________________")
    return "Printed"

#input sudoku board row-wise
def input_board():
    print("Enter sudoku\n")
    
    board = []												#empty sudoku board
    print("Enter elements (0 for empty cells)")
    print("Ex. 000800630")
    
    for i in range(1, 10):
        row = []
        text = input(f"Enter row {i}: ").strip()											
        for cell in text:
            row.append(int(cell))								#cells added in respective row
		
        board.append(row)									#row added in board    
    return board

def start():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Program to solve sudoku.")
        choice = input("Enter custom board(1) \nUse default one(2): ").strip()

        match choice:
            case '1' : 
                board = input_board()
                break
            case '2' : 
                board = boardo
                print("Using default board")
                break
            case default : 
                print("Wrong choice. Please enter again..")
        
    print_board(board)
    return board


def solve(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    # print_board(board)
    print(i)
    find = find_empty(board)
    if not find:
        return board
    else:
        row, col = find

    for i in range(1,10):
        if valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return board
            board[row][col] = 0

    return False


def valid(board, num, pos):
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check boardx
    boardx_x = pos[1] // 3
    boardx_y = pos[0] // 3

    for i in range(boardx_y*3, boardx_y*3 + 3):
        for j in range(boardx_x * 3, boardx_x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False

    return True



def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None


def hint(board):
    
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Hint ALGO menu. Enter ->")
            print("To reveal all '99': \nTo quit '-1': \nTo reveal position 'ij': ")
            h = int(input("Enter choice: "))
            if h < 0:
                return print_board(board)
            elif h > 88:
                print_board(board)
                input("Enter to continue: ")
            else:
                h = int(h)
                print("Val at", h, ":", board[int(h/10)][int(h%10)])
                input("Enter to continue: ")
        except:
            print("Enter valid value. i(0-8) is row value, j(0-8) is col value")            
            input("\nEnter to continue: ")
        

def main():
    board = start()
    board = solve(board)
    input("Press enter to remove solution: ")
    os.system('cls' if os.name == 'nt' else 'clear')
    hint(board)


if __name__ == "__main__":
	main()
