from tkinter import *
from tkinter import messagebox
from tkinter import font
import random
from PIL import ImageTk, Image

window = Tk()
window.title("Hangman")
lucida = font.Font(family='Lucida Handwriting', size=16)
comic_sans=font.Font(family='Comic Sans MS',size=16)
canvas = Canvas(window, width=700, height=600)
canvas.pack()

im = Image.open('graphics/background.png')  # background image
canvas.image = ImageTk.PhotoImage(im)  # Put the image into a canvas compatible class
canvas.create_image(0, 0, image=canvas.image, anchor='center')  # Add the image to the canvas

pole1 = canvas.create_line(65, 180, 65, 590, width=4)         # hangman gallows
pole2 = canvas.create_line(65, 180, 205, 180, width=4)
pole3 = canvas.create_line(205, 180, 205, 230, width=4)
status = canvas.create_text(210, 75, text="", font=lucida)
score=0
score_label=Label(canvas,text="Score: "+str(score),bg='#383434',fg='#0dc143',font=comic_sans,padx=10,pady=5)
score_label.place(x=450,y=54)


def exit():  # exit button callback
    window.destroy()


letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
words = ["hello","icecream","vanilla","strawberry","torch","butter","honey","umbrella","mountain","cloud","pizza","milk"]
hints = {"hello":"A Greeting","vanilla":"A flavour","strawberry":"A flavour","torch":"Gives light",
"icecream":"Cold and sweet","butter":"Used in baking cakes","honey":"Bees","mountain":"Hill","umbrella":"Rain",
"pizza":"Popular fast food","milk":"Goes well with oreos"}
guessed_letters = []   # holds guessed letters and their drawn objects
buttons = []   # holds letter buttons
blanks = []   # holds blank representation of the word
body_parts = []   # holds hangman body parts
letters_left = []  # letters left to be guessed in the word
score = 0
penalties_left = 6  # tries left
exit_button = Button(canvas, text="Exit", font=comic_sans, activebackground='white',activeforeground='#144fad',
                        bg='#144fad',fg='white',cursor='hand1',command=exit)
exit_button.place(x=600, y=50)


def draw_blanks(chosen_word):    # represents word as blanks
    offset = 0
    for letter in chosen_word:
        blank_letter = canvas.create_line(350 + offset, 250, 370 + offset, 250, width=4)
        blanks.append(blank_letter)
        offset = offset + 30
    return


def play_again():  # next button callback. clear screen and arrays for next word
    for el in guessed_letters:
        canvas.delete(el)         # delete drawn letters
    for el in blanks:
        canvas.delete(el)          # delete blanks
    for el in body_parts:
        canvas.delete(el)           # delete hangman parts
    guessed_letters.clear()
    canvas.itemconfig(status, text="")
    blanks.clear()
    buttons.clear()
    body_parts.clear()
    global penalties_left
    penalties_left = 6
    letters_left.clear()
    play()                          # next word


reset_button = Button(canvas, text="Next", font=comic_sans, activebackground='white', activeforeground='#144fad',
                 bg='#144fad', fg='white', cursor='hand1', command=play_again)
reset_button.place(x=400, y=530)


def letter_press(letter, chosen_word, letters_left):  # called when letter pressed
    canvas.itemconfig(status, text="")
    btn = buttons[ord(letter) - 97]       # deactivate button if already pressed
    btn.config(bg='#f4424b')
    if letter in guessed_letters:
        return
    if letter in chosen_word:
        letters_left[:] = (value for value in letters_left if
                           value != letter)  # removes all instances of pressed letter from letters_left
        fill_blanks(letter, chosen_word, letters_left)
    else:
        draw_penalty(chosen_word)
    guessed_letters.append(letter)
    return


def draw_penalty(chosen_word):  # wrong guess
    global penalties_left
    if penalties_left == 6:
        pic = PhotoImage(file='graphics/head.png')
        head=pic.subsample(2)
        canvas.create_image(195, 270, image=head)
        body_parts.append(head)
    elif penalties_left == 5:
        pic = PhotoImage(file='graphics/body.png')
        body = pic.subsample(3)
        canvas.create_image(195, 393, image=body)
        body_parts.append(body)
    elif penalties_left == 4:
        pic = PhotoImage(file='graphics/leftarm.png')
        larm = pic.subsample(5)
        canvas.create_image(120, 371, image=larm)
        body_parts.append(larm)
    elif penalties_left == 3:
        pic = PhotoImage(file='graphics/rightarm.png')
        rarm = pic.subsample(5)
        canvas.create_image(270, 369, image=rarm)
        body_parts.append(rarm)
    elif penalties_left == 2:
        pic = PhotoImage(file='graphics/rightleg.png')
        rleg = pic.subsample(5)
        canvas.create_image(223, 510, image=rleg)
        body_parts.append(rleg)
    else:
        pic = PhotoImage(file='graphics/leftleg.png')
        lleg = pic.subsample(5)
        canvas.create_image(153, 509, image=lleg)
        body_parts.append(lleg)
        canvas.itemconfig(status, text="You lose! Answer is "+chosen_word)

    penalties_left = penalties_left - 1
    return


def fill_blanks(letter, chosen_word, letters_left):
    indices = [i for i in range(len(chosen_word)) if chosen_word[i] == letter]
    # finds occurrence positions of letters
    for idx in indices:
        text = canvas.create_text(358 + idx * 30, 240, text=letter, font=lucida)  # draw letters
        guessed_letters.append(text)
    if letters_left == []:         # no letters left, win
        canvas.itemconfig(status, text="Good job!")
        global score
        score = score+1
        score_label.config(text="Score: "+str(score))
    return


def play():         # main gameplay loop
    chosen_word = random.choice(words)
    letters_left = list(chosen_word)
    offx, offy, c = 0, 0, 0
    for x in letters:  # creating letter buttons
        btn = Button(canvas, text=x.upper(), font=comic_sans, activebackground='white',activeforeground='#144fad',
                        bg='#144fad',fg='white', width=2, cursor='hand1',command=lambda x=x: letter_press(x, chosen_word, letters_left))
        # x=x so that lambda considers current value of x to pass not last value of x in loop
        btn.place(x=340 + offx, y=300 + offy)
        buttons.append(btn)
        offx = offx + 40
        c = c + 1
        if c == 7:
            c = 0
            offx = 0
            offy = offy + 50
    print(chosen_word)
    draw_blanks(chosen_word)

    def get_hint():
        messagebox.showinfo("Hint", hints[chosen_word])

    hint_button = Button(canvas, text="Hint", font=comic_sans, activebackground='white', activeforeground='#144fad',
                     bg='#144fad', fg='white', cursor='hand1', command=get_hint)
    hint_button.place(x=510, y=530)


play()
window.mainloop()
