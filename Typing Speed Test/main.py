from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os 

# ---------------------------- CONSTANTS ------------------------------- #
BUTTON_COLOR = "#93BFCF"
TEXT_COLOR = "#554994"
BACKGROUND_COLOR = "#BDCDD6"
FONT_NAME = "Courier"


# ---------------------------- VARIABLES ------------------------------- #
remaining_seconds = 60
all_words = []
on_screen_words = []
user_inputs = []
display_word_index = 0
mistakes = 0


# ---------------------------- FUNCTIONS ------------------------------ #

# Countdown mechanism for the test
def countdown_timer(seconds):
    global remaining_seconds
    remaining_seconds = seconds
    if seconds == 0:
        label_time.configure(text="Time's up!")
        # stop_test()
    else:
        label_time.configure(text=f"TIME: {seconds}")
        seconds -= 1
        window.after(1000, countdown_timer, seconds)


# Loading all the words from csv file for future use
def load_words():
    global all_words
    with open("words.csv", "r") as file:
        for n in file.readlines():
            all_words.append(n.replace('\n', '').lower())


# Get the highscore - return int value
def get_highscore():
    with open("high_score.txt", "r") as file:
        return int(file.read())


# Update highscore if user has bigger score
def set_highscore(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))


# Event listener: Process user input (count mistakes, change UI texts, ect...)
def on_text_changed(event):
    global user_inputs, on_screen_words, display_word_index, mistakes
    current_word_input = event.widget.get().lower()
    user_inputs.append(current_word_input) 

    # Clean input text field
    input_entry.delete(0, END)

    # Process stats for mistakes, wpm, cpm, score
    elapsed_time = 60 - remaining_seconds
    mistakes += calculate_mistakes_in_word(current_word_input, on_screen_words[display_word_index])
    raw_cpm = calculate_raw_cpm(elapsed_time)
    cpm = raw_cpm - mistakes
    wpm = calculate_wpm(elapsed_time, cpm)
    highscore = get_highscore()

    # End test if there is no more time left
    if remaining_seconds == 0:
        
        # Current score is bigger then previous highscore 
        if cpm > get_highscore():
            set_highscore(int(cpm))
            highscore = cpm
        # Update labels on UI
        label_mistakes.configure(text=f"MISTAKES: {mistakes}")
        label_cpm.configure(text=f"RAW CPM/CPM:: {raw_cpm:.0f}/{cpm:.0f}")
        label_wpm.configure(text=f"WPM: {wpm:.0f}")
        label_high_score.configure(text=f"SCORE: {highscore:.0f} NET WPM")
        stop_test()
    else:
        display_word_index += 1
        # Update labels on UI
        label_words.configure(text=on_screen_words[display_word_index])
        label_mistakes.configure(text=f"MISTAKES: {mistakes}")
        label_cpm.configure(text=f"RAW CPM/CPM: {raw_cpm:.0f}/{cpm:.0f}")
        label_wpm.configure(text=f"WPM: {wpm:.0f}")
        label_high_score.configure(text=f"SCORE: {highscore:.0f} NET WPM")


# Choose 200 random words for the test
def generate_words():
    global on_screen_words, all_words
    on_screen_words = random.sample(all_words, k=200)
    return on_screen_words


def calculate_wpm(elapsed_time, cpm):
    global user_inputs
    wpm = (cpm / 5) / (elapsed_time / 60)
    return wpm


def calculate_raw_cpm(elapsed_time):
    global user_inputs
    raw_cpm = len("".join(user_inputs)) / (elapsed_time / 60)
    return raw_cpm


def calculate_mistakes_in_word(input_word, answer_word):
    number_of_mistakes = 0
    # Return 0 mistakes, because the answer is correct
    if input_word == answer_word:
        return 0
    
    # User input is shorter than answer word
    if len(input_word) < len(answer_word):
        number_of_mistakes += (len(answer_word) - len(input_word))
        # Check mistakes inside the word
        for l_index, letter in enumerate(input_word):
            if letter != answer_word[l_index]:
                number_of_mistakes += 1
    
    # User input is longer than answer word OR 
    # User input lenght is equal with answer word lenght 
    else:
        number_of_mistakes += (len(input_word) - len(answer_word))
        # Check mistakes inside the word
        for l_index, letter in enumerate(answer_word):
            if letter != input_word[l_index]:
                number_of_mistakes += 1

    return number_of_mistakes


# Start the test
def start_test():
    global user_inputs, mistakes, display_word_index
    input_entry.focus()
    # Reset values
    user_inputs = []
    mistakes = 0
    display_word_index = 0
    countdown_timer(60)

    input_entry["state"] = "normal" 
    button_start["state"] = "disabled"
    # Update labels on UI
    label_words.configure(text=generate_words()[0])
    label_mistakes.configure(text=f"MISTAKES: 0")
    label_cpm.configure(text=f"RAW CPM/CPM:: --/--")
    label_wpm.configure(text=f"WPM: --")
    label_high_score.configure(text=f"SCORE: {get_highscore()} NET WPM")


# The test is over
def stop_test():
    input_entry["state"] = "disable" 
    button_start["state"] = "normal"
    label_words.configure(text="The test is over. Good job!\nPress the start button if you ready!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Typing Speed App")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# Load the words for the game
load_words()

# Current Statistics
label_time = Label(text=f"TIME: 60", bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 12, "bold"))
label_time.grid(column=0, row=0, sticky=W, columnspan=1, padx=(20, 0))
label_cpm = Label(text=f"RAW CPM/CPM: --/--", bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 12, "bold"))
label_cpm.grid(column=1, row=0, sticky=W, columnspan=1, padx=(40, 0))
label_wpm = Label(text=f"WPM: --", bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 12, "bold"))
label_wpm.grid(column=2, row=0, sticky=W, columnspan=1, padx=(40, 0))
label_mistakes = Label(text=f"MISTAKES: --", bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 12, "bold"))
label_mistakes.grid(column=3, row=0, sticky=W, columnspan=1, padx=(40, 0))
label_high_score = Label(text=f"SCORE: {get_highscore()} NET CPM", bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 12, "bold"))
label_high_score.grid(column=4, row=0, sticky=W, columnspan=1, padx=(40, 20))

# Exercise words
label_words = Label(text=f"Press the start button.\nAnd you can start typing", bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 16, "bold"), wraplength=1000)
label_words.grid(column=0, row=1, columnspan=5, padx=20, pady=(60, 30))

# Create an Entry widget and attach a callback function to its Modified event     
input_entry = Entry(window, state= "disabled", validate="key", width=120)
input_entry.bind("<Return>", on_text_changed)
# input_entry.bind("<Key>", on_text_changed)
input_entry.grid(column=0, row=2, sticky="nsew", columnspan=5, padx=20, pady=(30, 60))

# Start Button
button_start = Button(text="Start", command=start_test, highlightbackground=BACKGROUND_COLOR, fg=TEXT_COLOR, bg=BUTTON_COLOR, width=20, font=(FONT_NAME, 10, "bold"))
button_start.grid(column=4, row=3)









window.mainloop()