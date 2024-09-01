print('''
 _____ _        _____            _____          
|_   _(_)      |_   _|          |_   _|         
  | |  _  ___    | | __ _  ___    | | ___   ___ 
  | | | |/ __|   | |/ _` |/ __|   | |/ _ \ / _ \\
  | | | | (__    | | (_| | (__    | | (_) |  __/
  \_/ |_|\___|   \_/\__,_|\___|   \_/\___/ \___|

''')

clean_pos_state = {
    1: " ", 2: " ", 3: " ",  # Top 3 position
    4: " ", 5: " ", 6: " ",  # Middle 3 positio
    7: " ", 8: " ", 9: " ",  # Bottom 3 position
} 

p1_score = 0 
p2_score = 0


# Prints the current state of the game 
def print_state():
    print(f" {pos_state[1]} | {pos_state[2]} | {pos_state[3]}")
    print("- - - - - -")
    print(f" {pos_state[4]} | {pos_state[5]} | {pos_state[6]}")
    print("- - - - - -")
    print(f" {pos_state[7]} | {pos_state[8]} | {pos_state[9]}")


def check_winning():
    # Checking rows
    if pos_state[1] == pos_state[2] == pos_state[3] and pos_state[1] != " ":
        return True
    if pos_state[4] == pos_state[5] == pos_state[6] and pos_state[4] != " ":
        return True
    if pos_state[7] == pos_state[8] == pos_state[9] and pos_state[7] != " ":
        return True
    
    # Checking columns
    if pos_state[1] == pos_state[4] == pos_state[7] and pos_state[1] != " ":
        return True
    if pos_state[2] == pos_state[5] == pos_state[8] and pos_state[2] != " ":
        return True
    if pos_state[3] == pos_state[6] == pos_state[9] and pos_state[3] != " ":
        return True
    
    # Checking crosses
    if pos_state[1] == pos_state[5] == pos_state[9] and pos_state[5] != " ":
        return True
    if pos_state[3] == pos_state[5] == pos_state[7] and pos_state[5] != " ":
        return True
    
    # Return false if there is no winner currently
    return False


# Start a new game until the users want to play an another match
while str(input("Do you wanna play? (Y/N) ")).lower() == "y":
    # This matches state
    pos_state = dict(clean_pos_state)

    # Shows the users the current scoreboard
    print(f"\nScoreboard:\nPlayer_1 : {p1_score}  -  Player_2 : {p2_score}\n")

    # play the match rounds until there is a winner or no free place left
    for i in range(9):
        # Shows the current state of the game 
        print_state()

        # Switch players based on the number of turns
        current_player = "X"
        if i % 2 == 0:
            current_player = "X"
        else:
            current_player = "O"
        
        # Ask a user for the next move and check that the answer is valid
        answer_not_valid = True
        while answer_not_valid:
            try:
                chosen_pos = int(input("\nEnter the number of your next loaction (1-9): "))
                if pos_state[chosen_pos] == " ":
                    answer_not_valid = False
                else:
                    print("The location must be empty!")
            except:
                print("Enter a number between 1 and 9!")
        pos_state[chosen_pos] = current_player
        
        # Stop the match if there is a winner
        if check_winning():
            
            if current_player == "X":
                p1_score += 1
                print("\n=====================\nWinner is Player 1 (X)!\n=======\n")
            else:
                p2_score += 1
                print("\n=====================\nWinner is Player 2 (O)!\n=======\n")
            break
        
        # The match has ended and it is a tie
        if i == 8:
            print("\n=====================\nThis is a tie!\n=======\n")
            
    # Shows the current state of the game 
    print_state()
    # Shows the users the current scoreboard
    print(f"\nScoreboard:\nPlayer_1 : {p1_score}  -  Player_2 : {p2_score}\n")



