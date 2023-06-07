from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"

# Data Management and functions

try:
    previous_data = open("./data/words_to_learn.csv")
    words_dataframe = pandas.read_csv(previous_data)
except FileNotFoundError:
    words_dataframe = pandas.read_csv("./data/french_words.csv")

words_dictionary = words_dataframe.to_dict(orient="records")
current_card = choice(words_dictionary)


def show_new_word():
    """
    Shows a new card with another word to study.
    :return: a dictionary of the new word with its equivalent in foreign language. E.G. {'partie':'part'}
    """
    global current_card, timer
    window.after_cancel(timer)
    current_card = choice(words_dictionary)
    selected_word = current_card["French"]
    card_container.itemconfig(title_text, text="French", fill="black")
    card_container.itemconfig(word_text, text=selected_word, fill="black")
    card_container.itemconfig(card_image, image=card_front_image)
    timer = window.after(3000, flip_card)
    return current_card


def save_correct_response():
    """
    Activates when the users hit the green button. It removes any known word and create a dataframe and csv file.
    """
    guessed_card = show_new_word()
    words_dictionary.remove(guessed_card)
    answers_dataframe = pandas.DataFrame(words_dictionary)
    answers_dataframe.to_csv("./data/words_to_learn.csv", index=False)


def flip_card():
    """
    Changes the side of the card to translate the word.
    :return:
    """
    translated_word = current_card["English"]
    card_container.itemconfig(card_image, image=card_back_image)
    card_container.itemconfig(title_text, text="English", fill="white")
    card_container.itemconfig(word_text, text=translated_word, fill="white")


# User Interface
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

timer = window.after(3000, func=flip_card)

card_container = Canvas(window, width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")
card_image = card_container.create_image(400, 263, image=card_front_image)
card_container.grid(column=0, row=0, columnspan=2)


title_text = card_container.create_text(400, 150, text="French", font=('Ariel', '40', 'italic'))
word_text = card_container.create_text(400, 270, text=current_card["French"], font=('Ariel', '60', 'bold'), tags='word')


wrong_button_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=show_new_word)
wrong_button.grid(column=0, row=1)

right_button_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_button_image, highlightthickness=0, command=save_correct_response)
right_button.grid(column=1, row=1)


window.mainloop()
