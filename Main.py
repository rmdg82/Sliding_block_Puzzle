# A solver for a generic n*n block puzzle 
# Exercise to implement various kinds of search (DFS, BFS, A*, IDA*, etc)

import random
import copy
import time
import Game as G
import Heuristics as H

# Initialize a variable used to track execution time 
starting_date = ""


# Functions
def execute(game, move):
    '''Execute a move(str) in a game.
	'''
    if move == "right":
        game.right()
    elif move == "left":
        game.left()
    elif move == "up":
        game.up()
    elif move == "down":
        game.down()
    else:
        print("Move not recognized!")


def argmin(game, heuristic):
    '''Given a game (with a game.state) and an heuristic return the possible move as a string with the min value of heuristic.
	We execute all the possible moves in a copied game and we pick the minimum heuristic value.
	'''
    # Dictionary with all possible moves as a key and heuristic as a value
    hmoves = dict.fromkeys(game.valid_moves())
    # Deepcopy the game in order to not modify the original obj
    for key in hmoves.keys():
        copied_game = copy.deepcopy(game)
        execute(copied_game, key)
        hmoves[key] = heuristic.AStar_distance(copied_game.state)
        del copied_game
    # Return non-decreasing-ordered by value dict hmoves
    return sorted(hmoves.items(), key=lambda x: x[1])


def pick(game, heuristic):
    '''Choose, given a game and heuristic, the transition state from game.state with the min heuristic value.
	It also check if the state to reach has already been reached in the past, comparing with a game.explored list of states.
	 '''
    argmin_list = argmin(game, heuristic)
    # Create min_list which will contain all the items with the min value.
    # Then we will shuffle them and append to the begining of argmin_list, just to have some randomness to avoid loops
    min_val = argmin_list[0][1]
    min_list = []
    for item in argmin_list:
        if item[1] == min_val:
            min_list.append(item)
    random.shuffle(min_list)
    # Remove from argmin_list the min values and concatenate the shuffled min_list at the beginning
    argmin_list = [item for item in argmin_list if item[1] != min_val]
    argmin_list = min_list + argmin_list
    # Create a new game, deepcoping the original one
    new_argmin_list = []
    for items in argmin_list:
        copied_game = copy.deepcopy(game)
        candidate = items[0]
        execute(copied_game, candidate)
        # Check if the state has already been reached (is in game.explored)
        if copied_game.state not in game.explored:
            new_argmin_list.append(items)
        del copied_game
    if len(new_argmin_list) == 0:
        return False
    else:
        return new_argmin_list[0][0]


def backpath(game):
    return game.state.previous_actions


def from_list_to_state(orderedValues, size):
    '''	From a list return a state with table values got in order from that list.
	'''
    # Check consistency between number of values and size of table
    assert len(orderedValues) == size ** 2, "List lenght not compatible with the size of the state.table"
    # Check consistency into the values in the list
    admissible_values = [i for i in range(size ** 2)]
    for i in admissible_values:
        if orderedValues.count(i) != 1:
            raise ValueError
    # Creata a size*size table filled with 0's
    table = [[0 for i in range(size)] for i in range(size)]
    count = 0
    for row in range(size):
        for col in range(size):
            table[row][col] = int(orderedValues[count])
            count += 1
    return G.State(table, size)


def search(game, heuristic, attempt=1, depth=250):
    '''Best-first search with A* heuristic. Depth represents the max number of moves allowed before deciding to start the search again.
	'''
    steps = 0
    start_time = time.time()
    while game.check_solution() != True:
        move = pick(game, heuristic)
        if (move == False) or (steps > depth):
            print(f"No solution found! Attempt number {attempt}")
            if move == False:
                print("Got stuck in the middle of nowhere :(")
            else:
                print(f"Fixed depth of {depth} excedeed.")
            print("I searched", len(game.state.previous_actions), "states.")
            return False
        print("Chosen move:", move)
        execute(game, move)
        steps += 1
        game.print()
        print("Move number:", steps)
        print("Heuristic value:", heuristic.AStar_distance(game.state), "\n")
    if game.check_solution():
        time_elapsed = round(time.time() - start_time, 2)
        print(f"Solution found in {time_elapsed} seconds at the attempt number {attempt}!")
        print("Initial state:")
        game.explored[0].print()
        print(f"Solution of length {len(backpath(game))} found:\n", backpath(game))
        print(f"Search started at {starting_date} and ended at", time.asctime(time.localtime(time.time())))
        return True


# MAIN
def main():
    print("Sliding Puzzle Solver!\n")
    # Get size of the board from user
    size = int()
    while True:
        try:
            size = int(input("Insert the size of the board:"))
            if size < 2:
                raise ValueError
            else:
                break
        except ValueError:
            print("Insert a positive natural number > 1 !")
            continue

    game = G.Game(size)
    heuristic = H.Heuristics(game)

    inserted_value = str()
    inserted_position = []
    initial_state = None

    # Get the initial state (doesn't check the user input properly :()
    while not (inserted_value.upper() == 'Y') or (inserted_value.upper() == 'N'):
        inserted_value = input("Would you like to start from a random position (Y/N)?").upper()
        if inserted_value == 'Y':
            # Start with a random initial position
            game.shuffle()
            # Save the initial state/table
            initial_state = copy.deepcopy(game.state)
            break
        if inserted_value.upper() == 'N':
            for i in range(size ** 2):
                value = input(f"Insert the value number {i + 1}: ")
                try:
                    inserted_position.append(int(value))
                except ValueError:
                    print("Insert a positive natural number! Exiting ...")
                    break

            s = from_list_to_state(inserted_position, size)
            game.set_state(s)
            initial_state = copy.deepcopy(game.state)
            break

    game.set_state(initial_state)
    print("Initial state:")
    game.print();
    print()

    input("Press Enter to continue ...")
    starting_date = time.asctime(time.localtime(time.time()))
    print(f"Start searching at {starting_date}", )
    time.sleep(1)
    searching = True
    attempt = 1

    # Search routine
    while searching:
        searching = not search(game, heuristic, attempt)
        # If search return False executes the following if clause
        if searching:
            print("I'll try again from:")
            # Clean the game and set the previous initial state
            attempt += 1
            game.set_state(initial_state)
            game.explored = []
            game.state.previous_actions = []
            game.print();
            print()
            print("Start again in 2 seconds ...")
            time.sleep(2)
            # input("Press Enter to continue ...")
            searching = True
            continue


if __name__ == "__main__":
    main()
else:
    print("Module imported, main() not executed!")
