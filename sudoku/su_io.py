def main():
	board = input_board()
	print_board(board)
	

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
            row.append(cell)								#cells added in respective row
		
        board.append(row)									#row added in board
    
    return board



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
                print(str(board[i][j]) + " ", end="")
    print("____________________________")
    


if __name__ == '__main__':
    main()
