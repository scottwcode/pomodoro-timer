# pomodoro-timer
# This program is an app to simulate a pomodoro timer for work & break
# time management. Pomodoro is italian for tomato (thus the image)
# and the timer is broken down into intervals based on the book
# The Pomodoro Technique. These intervals and colors can be adjusted in the
# constants part of the code
#   WORK_MIN - Time spent working
#   SHORT_BREAK_MIN - After an allocated time for work, the timer shifts to break
#   LONG_BREAK_MIN - Each 4th work/shortbreak interval, there is a longer break
#

from tkinter import *
# from PIL import ImageTk, Image
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
# WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


def reset_timer():
    """ Resets the timer and appropriate labels"""
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps = 0


def start_timer():
    """ The timer that sets the time and label displayed """
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)


def count_down(count):
    """ Performs a countdown each second (1000 ms) and sets the timer in min:sec """
    global reps, timer

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    # print(count)
    if count > 0:
        # For testing, can have faster timer below
        # timer = window.after(10, count_down, count - 1)
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔︎"
        check_marks.config(text=marks)


# Window frame setup
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
title_label = Label(text="Timer", fg=GREEN, bg=YELLOW,
                    font=(FONT_NAME, 50, "bold"))
title_label.grid(column=1, row=0)

# Create canvas similar in size to the image
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.gif")
# tomato_img = ImageTk.PhotoImage(Image.open("tomato.gif"))
canvas.create_image(100, 112, image=tomato_img)

# Timer label
timer_text = canvas.create_text(100, 130, text="00:00", fill="white",
                                font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)


# Buttons to start and reset the timer
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

# Check marks for each session completed
check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

window.mainloop()
