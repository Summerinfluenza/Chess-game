from os import system, name
from Board import Board


# Clear the board
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')


# Creating a play board
board = Board()
board.default_board()
board.print_board()


while True:
    # If the player is checked at the start of their turn
    if board.check():
        # Checking if the player is checkmated
        if board.check_mate():
            print("Game over: Checkmated")
            break

    # Receiving player inputs and checks if it's a valid move according to the rules

    if board.player_move():
        clear()
        board.turn_count += 1
    else:
        clear()
        print("Invalid move")

    # Printing the results
    if board.turn_count % 2 == 0:
        board.player_turn = "white"
    else:
        board.player_turn = "black"

    if board.check():
        board.status = "checked"
    else:
        board.status = ""

    board.print_board()