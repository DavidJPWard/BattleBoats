"""
this is battle boats, this file contains the functions to play the game as
well as an abstract class named playerboard and two inherited classes I have
imported for a human and computer player. random is an external library I
have imported
"""
import random
from scripts.Player_Board import Player_Board
from scripts.Computer_Board import Computer_Board

boardSize = 5
sub_num = 5
frig_num = 2


def populate_board(board, num_of_subs, num_of_frigates):
    """
    randomly populates the game board with subs and frigates.

    subs are created by checking a random set of co-ordinates on the board
    is free, if yes, that location is added to a list of ships(used for
    logic checking) and a list of subs(used to mark its location on the
    board).

    frigates are created by then making essentially a sub, but then picking
    a random direction for the second tile, if those co-ordinates are free
    then both sets of co-ordinates are added to the list of ships and list
    of frigates.
    """
    i = 0
    while i < int(num_of_subs):
        new_sub = random.randint(
            0, board.size-1
        ), random.randint(0, board.size-1)
        if new_sub not in board.ships:
            board.subs.append(new_sub)
            board.ships.append(new_sub)
            i += 1
    i = 0
    while i < int(num_of_frigates):
        new_big_ship_x = random.randint(0, board.size-1)
        new_big_ship_y = random.randint(0, board.size-1)
        new_frigate = new_big_ship_x, new_big_ship_y

        if new_frigate not in board.ships:
            timeout = 0

            while timeout < 4:
                direction = random.randint(1, 4)

                if direction == 1:
                    if new_big_ship_x + 1 <= boardSize-1 and (
                        new_big_ship_x + 1, new_big_ship_y
                    ) not in board.ships:
                        new_frigate_part_2 = new_big_ship_x + 1, new_big_ship_y
                        board.frigates.append(new_frigate)
                        board.ships.append(new_frigate)
                        board.frigates.append(new_frigate_part_2)
                        board.ships.append(new_frigate_part_2)
                        i += 1
                        break
                elif direction == 2:
                    if new_big_ship_y + 1 <= boardSize-1 and (
                        new_big_ship_x, new_big_ship_y + 1
                    ) not in board.ships:
                        new_frigate_part_2 = new_big_ship_x, new_big_ship_y + 1
                        board.frigates.append(new_frigate)
                        board.ships.append(new_frigate)
                        board.frigates.append(new_frigate_part_2)
                        board.ships.append(new_frigate_part_2)
                        i += 1
                        break
                elif direction == 3:
                    if new_big_ship_x - 1 >= 0 and (
                        new_big_ship_x - 1, new_big_ship_y
                    ) not in board.ships:
                        new_frigate_part_2 = new_big_ship_x - 1, new_big_ship_y
                        board.frigates.append(new_frigate)
                        board.ships.append(new_frigate)
                        board.frigates.append(new_frigate_part_2)
                        board.ships.append(new_frigate_part_2)
                        i += 1
                        break
                elif direction == 4:
                    if new_big_ship_y - 1 >= 0 and (
                        new_big_ship_x, new_big_ship_y - 1
                    ) not in board.ships:
                        new_frigate_part_2 = new_big_ship_x, new_big_ship_y - 1
                        board.frigates.append(new_frigate)
                        board.ships.append(new_frigate)
                        board.frigates.append(new_frigate_part_2)
                        board.ships.append(new_frigate_part_2)
                        i += 1
                        break
                timeout += 1
    board.num_of_ships = num_of_subs + num_of_frigates * 2


def play_game(player_board, computer_board):
    """
    called when the game has finished setting up, calls for guesses to be continously
    entered via a loop and breaks when either players score equals the number of ships.
    """
    player_board.display_player_ships()

    player_score = 0
    computer_score = 0
    while player_score < int(
        player_board.num_of_ships
    ) and computer_score < int(computer_board.num_of_ships):
        computer_board.print_board()
        player_board.print_board()

        if computer_board.guesses:
            print(f"Player Score: {player_score}, Computer Score : {computer_score}")
            num_of_guesses = computer_board.print_player_guesses()
            if num_of_guesses == boardSize * boardSize:
                break

        print("\n")

        x, y = make_guess(computer_board)

        while True:
            computer_x_guess = random.randint(0, boardSize-1)
            computer_y_guess = random.randint(0, boardSize-1)

            if is_new_coordinates(computer_x_guess, computer_y_guess, player_board):
                break

        if computer_board.guess_against(x, y, player_board) is True:
            player_score += 1

        if player_board.guess_against(
            computer_x_guess, computer_y_guess, computer_board
        ) is True:
            computer_score += 1

    computer_board.print_board()
    player_board.print_board()

    print("\n")

    if player_score == computer_score:
        print("game was a draw")
    elif player_score >= player_board.num_of_ships:
        print(f"{player_board.name} has won\n")
    elif computer_score >= computer_board.num_of_ships:
        print(f"{computer_board.name} has won\n")

    input("please any key to continue")
    menu()


def make_guess(board):
    """
    function that creates a tuple out of the inputs made by the player,
    checks they are valid and returns it
    """
    while True:
        while True:
            x_guess = input(f"please choose an x coordinate(a number between 0 and {boardSize -1}): ")
            if validate_int(x_guess, 1, 0, board.size - 1) is True:
                break
            print("please pick again")

        while True:
            y_guess = input(f"please choose an y coordinate(a number between 0 and {boardSize-1}): ")
            if validate_int(y_guess, 1, 0, board.size - 1) is True:
                break
            print("please pick again")

        if is_new_coordinates(x_guess, y_guess, board) is True:
            break

    return x_guess, y_guess


def menu():
    """
    Main menu of the game, here you can change settings and start a game.
    """
    global boardSize
    global sub_num
    global frig_num

    print("           " + "-" * 35)
    print("               Welcome to BATTLE BOATS")
    print(f"           board size: {boardSize}, subs: {sub_num} frigates: {frig_num}")
    print("           " + "-" * 35)
    print("q: Start Game    w: Change Board Size    e: Change Ship Number \n")

    option = input("Please choose and option: ").lower()

    while True:
        if option in ("q", "w", "e"):
            break
        print("Invalid option, please press q, w or e\n")
        option = input("Please choose and option: ").lower()

    if option == "q":
        new_game()
    elif option == "w":
        boardSize = int(change_board_size())
        menu()
    elif option == "e":
        sub_num, frig_num = change_ship_num()
        menu()


def change_board_size():
    """
    simply takes a value from input and assigns it to the BoardSize variable
    """
    print("please pick a number between 5 and 10 to change the game board")
    while True:
        new_size = input()
        if validate_int(new_size, 2, 5, 10):
            break
        print("Please pick another number between 5 and 10 ")
    return new_size


def change_ship_num():
    """
    simply takes a value from input and assigns it to the BoardSize function
    """
    print("how many subs would you like? (pick a number between 1 and 6)")
    while True:
        new_sub_num = input()
        if validate_int(new_sub_num, 1, 1, 6):
            break
        print("Please pick another number between 1 and 6")

    print("how many frigates would you like? (pick a number between 1 and 3)")

    while True:
        new_frig_num = input()
        if validate_int(new_frig_num, 1, 1, 3):
            break
        print("Please pick another number between 1 and 4")

    return new_sub_num, new_frig_num


def validate_str(string):
    """
    validates strings, making sure no numbers or special chracters are present
    """
    if string.isalpha():
        return True
    print("your name cannot contain numbers of special symbols")
    return False


def validate_int(int_for_validation, length, min_value, max_value):
    """
    validates interger values, checks if the input is an interger and
    that it doesnt exceed its target length, or value range
    """
    try:
        if str(int_for_validation).isdigit() is not True:
            raise ValueError(f"input must be an integer")
        int_for_validation = int(int_for_validation)
        if len(str(int_for_validation)) > length:
            raise ValueError(f"input has exceeded the maximum length of {length} chracters")
        if int_for_validation < min_value:
            raise ValueError(f"input cannot be less than {min_value}")
        if int_for_validation > max_value:
            raise ValueError(f"input cannot be more than {max_value}")
    except ValueError as e:
        print(f"Invalid: {e}\n")
        return False
    return True


def is_new_coordinates(x, y, board):
    """
    checks if a set of co ordinates have already been guessed, returns true if
    they were new.
    """
    entry = [int(x), int(y)]
    if entry not in board.guesses:

        return True
    else:
        if board.type == "computer":
            print(f"co-ordinates ({x}, {y}) have already been guessed, pick again\n")
        return False


def new_game():
    """
    called when a new game is started, creates 2 boards, one for each
    player, and populates them with ships. then calls the play game function.
    """
    while True:
        player_name = input("What is your name?: ")
        if validate_str(player_name):
            break

    print("\n")
    shipNum = frig_num * 2 + sub_num
    player_board = Player_Board(player_name, boardSize, shipNum, "player")
    computer_board = Computer_Board("computer", boardSize, shipNum, "computer")
    player_board.board.reverse()
    computer_board.board.reverse()

    populate_board(player_board, sub_num, frig_num)
    populate_board(computer_board, sub_num, frig_num)

    play_game(player_board, computer_board)


def main():
    """
    Main function
    """
    menu()


main()
