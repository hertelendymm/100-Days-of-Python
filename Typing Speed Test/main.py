from tkinter import *
from tkinter import filedialog
import os 
from tkinter import messagebox
from PIL import Image,ImageTk
import random

# ---------------------------- CONSTANTS ------------------------------- #
BUTTON_COLOR = "#93BFCF"
TEXT_COLOR = "#554994"
BACKGROUND_COLOR = "#BDCDD6"
RED = "#ff0000"
FONT_NAME = "Courier"

remaining_seconds = 60
cpm_text = 0
wpm_text = 0
mistakes_text = 0
high_score_text = 0
all_words = []
on_screen_words = []
user_input = []


# ---------------------------- FUNCTIONS ------------------------------ #

# Countdown mechanism for the test
def countdown_timer(seconds):
    global remaining_seconds
    remaining_seconds = seconds
    if seconds == 0:
        label_time.configure(text="Time's up!")
        stop_test()
    else:
        label_time.configure(text=f"TIME: {seconds}")
        seconds -= 1
        window.after(1000, countdown_timer, seconds)


# Loading all the words from csv file for future use
def load_words():
    global all_words
    with open("words.csv", "r") as file:
        for n in file.readlines():
            all_words.append(n.replace('\n', ''))


# Choose 40 random words for the test
def generate_words():
    global on_screen_words, all_words
    on_screen_words = random.sample(all_words, k=40)
    print(on_screen_words)
    return " ".join(on_screen_words)


# Start the test
def start_test():
    global user_input
    user_input = []
    input_entry["state"] = "normal" 
    button_start["state"] = "disabled"
    countdown_timer(60)
    label_words.configure(text=generate_words())


# The test is over
def stop_test():
    input_entry["state"] = "disable" 
    button_start["state"] = "normal"
    label_words.configure(text="The test is over. Good job!")


# Event listener: Process user input (count mistakes, change UI texts, ect...)
def on_text_changed(event):
    global user_input, on_screen_words, mistakes_text
    current_text_input = event.widget.get()
    user_input = current_text_input.lower().split(" ")
    mistakes_text = 0

    for word_index, word in enumerate(user_input):
        for letter_index in range(len(word)):
            # Skip checking letters that are outside of the answer words length
            if letter_index >= len(on_screen_words[word_index]):
                mistakes_text += 1
                break

            # Add mistakes +1 each time a finished word is less than answer word, except the the last word
            if letter_index < len(on_screen_words[word_index]) and word_index != len(user_input)-1:
                mistakes_text += 1

            # Add mistakes +1 each time letter does not match with letter in answer word
            print(word[letter_index], on_screen_words[word_index][letter_index])
            if word[letter_index] != on_screen_words[word_index][letter_index]:
                mistakes_text += 1

    # Update labels on UI
    label_words.configure(text=on_screen_words[len(user_input)-1:])
    label_mistakes.configure(text=f"MISTAKES: {mistakes_text}")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Typing Speed App")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# Load the words for the game
load_words()

# Current Statistics
label_time = Label(text=f"TIME: 60", bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 12, "bold"))
label_time.grid(column=0, row=0, sticky=W, columnspan=1, padx=(20, 0))
label_cpm = Label(text=f"CPM: {cpm_text}", bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 12, "bold"))
label_cpm.grid(column=1, row=0, sticky=W, columnspan=1, padx=(40, 0))
label_wpm = Label(text=f"WPM: {wpm_text}", bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 12, "bold"))
label_wpm.grid(column=2, row=0, sticky=W, columnspan=1, padx=(40, 0))
label_mistakes = Label(text=f"MISTAKES: {mistakes_text}", bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 12, "bold"))
label_mistakes.grid(column=3, row=0, sticky=W, columnspan=1, padx=(40, 0))
label_high_score = Label(text=f"HIGH SCORE: {high_score_text} NET WPM", bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 12, "bold"))
label_high_score.grid(column=4, row=0, sticky=W, columnspan=1, padx=(40, 20))

# Exercise words
label_words = Label(text=f"Press the start button. And you can start typing", bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 16, "bold"), wraplength=1000)
label_words.grid(column=0, row=1, columnspan=5, padx=20, pady=(60, 30))

# Create an Entry widget and attach a callback function to its Modified event
input_entry = Entry(window, state= "disabled", validate="key", width=120)
input_entry.bind("<Key>", on_text_changed)
input_entry.grid(column=0, row=2, sticky=W, columnspan=5, padx=20, pady=(30, 60))

# Start Button
button_start = Button(text="Start", command=start_test, highlightbackground=BACKGROUND_COLOR, fg=TEXT_COLOR, bg=BUTTON_COLOR, width=20, font=(FONT_NAME, 10, "bold"))
button_start.grid(column=4, row=3)









window.mainloop()