import random
import time
import tkinter as tk
import turtle
from tkinter import messagebox

# Global Functions

# Converts seconds to string statement of hours:minutes:seconds

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  return f"{int(hours)}:{int(mins)}:{round(sec,2)}"

# Open csv file to retrieve data and place all in dictionary

def convert_data_from_file():
    ls_out = []
    with open("fruits_dictionary.csv", "r") as f:
        # Seperate each line of the file into elements of a list
        ls = f.read().split("\n")
        # First line used as keys
        ls_key = ls[0].split(",")
        # First element excluded as they are keys, last element excluded as they are blanks
        for i in range(1, len(ls)-1):
            ls_value = ls[i].split(",")
            # Zip the key-value pairs in dict_in for each planning, and combine all inside dict_out
            dict_in = dict(zip(ls_key, ls_value))
            ls_out.append(dict_in)
        return ls_out

#global variables
time_lapsed = ""
player_name = ""
current_card = ""
test_dict_original = convert_data_from_file()
test_dict = test_dict_original.copy()
learnt_words = []
retry_count = 0

#classes(Screens)
class Start_Screen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Loading Screen...")
        self.root.geometry("250x200")

        self.label = tk.Label(self.root, text="Enter your Name: ", font=('Poppins', 15))
        self.label.pack(padx=10, pady=10)

        global player_name
        player_name = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable= player_name, font=('Poppins', 10))
        self.entry.bind("<KeyPress>", self.Enter_shortcut)
        self.entry.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text="Enter ", font=('Poppins', 15),command=self.update)
        self.button.pack(padx=10,pady=10)

        self.root.mainloop()

    # You can finally use the enter key to enter your name in the textbox
    def Enter_shortcut(self,event):
        print(event.keysym)
        if event.keysym == "Return":
            self.update()

    #Username confirmation screen
    def update(self):
        result = tk.messagebox.askyesno(
            title= "Confirmation Screen",
            message= "Go with this name?",
            detail="Click 'No' to quit"
        )
        if result == True:
            global player_name
            player_name = self.entry.get()
            self.root.withdraw()
            Main_Menu_Screen()

class Main_Menu_Screen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bing Chilling Flashcards")
        self.root.geometry("600x450")

        self.label2 = tk.Label(self.root,text=f"Welcome, {player_name}!",font=("Poppins",15))
        self.label2.pack(padx=5,pady=5)

        self.label = tk.Label(self.root,text= "BING CHILLING!", font=("Poppins", 40, "italic","bold"))
        self.label.pack(padx=10,pady=40)

        self.Play_Button = tk.Button(self.root, text="Play",font=("Poppins", 12),command=self.to_gameplay)
        self.Play_Button.pack(padx=10,pady=10)

        self.Credits_Button = tk.Button(self.root, text="Credits", font=("Poppins", 12), command=Credits_Screen)
        self.Credits_Button.pack(padx=10, pady=10)

        self.Exit_Button = tk.Button(self.root, text="Exit",font=("Poppins", 12),command=self.exit)
        self.Exit_Button.pack(padx=10,pady=10)

    #Exit Confirmation Screen
    def exit(self):
        result = tk.messagebox.askyesno(
            title="Confirmation Screen",
            message="Exit Game?",
            detail="Click 'No' to quit"
        )
        if result == True:
            exit()

    #Close main menu, go to Gameplay_Screen
    def to_gameplay(self):
        self.root.withdraw()
        Gameplay_Screen()

class Gameplay_Screen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gameplay")
        self.root.config(padx=20,pady=20)

        self.canvas = tk.Canvas(self.root, width=800, height=400)
        self.card_title = self.canvas.create_text(400, 150, text="How to Play",font=("Poppins", 40, "italic","bold"))
        self.card_word = self.canvas.create_text(400, 250, text=
        "- Guess the English translation of the given word on the flashcard -\n"
        "Reveal - Reveal back of flashcard\n"
        "Correct - Removes flashcard pair from the deck\n"
        "Test again - Flashcard pair is reshuffled into the deck", font=("Poppins", 15))
        self.canvas.config(highlightthickness=0)
        self.canvas.grid(row=0,column=0,columnspan=3)

        self.Start_Button = tk.Button(self.root, text="Start Game", font=("Poppins", 20), command=self.start_flashcards)
        self.Start_Button.grid(row=1, column=1)

        # Below Buttons are hidden until start/reveal answer is pressed
        self.Reveal_Button = tk.Button(self.root, text="Reveal", font=("Poppins", 20), command=self.reveal_answer)
        self.Correct_Button = tk.Button(self.root, text="Correct", font=("Poppins", 20),command=self.remove_from_list)
        self.Wrong_Button = tk.Button(self.root, text="Test again", font=("Poppins", 20,),command=self.test_yourself_again)

    # Starts the Game and reveals the reveal answer button, including the timer, for player Report
    def start_flashcards(self):
        global current_card
        current_card = random.choice(test_dict)
        self.canvas.itemconfig(self.card_title, text="Chinese",font=("Poppins", 40, "italic"))
        self.canvas.itemconfig(self.card_word, text=current_card["Chinese"],font=("Poppins", 60, "bold"))
        self.Reveal_Button.grid(row=2, column=1)
        self.Start_Button.grid_forget()
        self.start_time=time.time()

    # Reveals the other Key and Value of the dictionary to be tested, hides reveal button,
    # show the other 2 buttons - Remove from List & Test Yourself Again
    def reveal_answer(self):
        global current_card
        self.canvas.itemconfig(self.card_title, text="English")
        self.canvas.itemconfig(self.card_word, text=current_card["English"])
        self.Reveal_Button.grid_forget()
        self.Correct_Button.grid(row=2, column=0)
        self.Wrong_Button.grid(row=2, column=2)

    # Removes current card(dictionary) from dictionary to learn, so player
    # does not get tested again, and appends it to list with words learnt, for player Report
    def remove_from_list(self):
        global current_card
        global test_dict
        try:
            test_dict.remove(current_card)
            learnt_words.append(current_card)
            current_card = random.choice(test_dict)
            self.canvas.itemconfig(self.card_title, text="Chinese")
            self.canvas.itemconfig(self.card_word, text=current_card["Chinese"])
    # After running out of cards to be tested, timer ends and the Result Screen shows.
    # It will cause an IndexError because once test_dict is [], random choice picks a random index from an empty list
        except IndexError:
            self.end_time=time.time()
            global time_lapsed
            time_lapsed = self.end_time - self.start_time
            time_lapsed = time_convert(time_lapsed)
            print(time_lapsed)
            self.root.withdraw()
            Report_Screen()
        self.Reveal_Button.grid(row=1, column=1)
        self.Correct_Button.grid_forget()
        self.Wrong_Button.grid_forget()

    #Pressing "Test yourself" increases the counter by 1, for player Report
    def test_yourself_again(self):
        global retry_count
        retry_count += 1
        global current_card
        global test_dict
        current_card = random.choice(test_dict)
        self.canvas.itemconfig(self.card_title, text="Chinese")
        self.canvas.itemconfig(self.card_word, text=current_card["Chinese"])
        self.Reveal_Button.grid(row=1, column=1)
        self.Correct_Button.grid_forget()
        self.Wrong_Button.grid_forget()

class Report_Screen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Report Screen")
        self.root.geometry("500x600")

        self.canvas = tk.Canvas(self.root, width=450, height=450)
        self.canvas.pack(side=tk.TOP)
        # If Test yourself wasnt clicked at all, show happy face. Otherwise, it will show sad face.
        if retry_count < 3:
            self.label = tk.Label(self.root, text=f"Well done, {player_name}!", font=("Poppins", 15))
            self.label.pack(padx=10, pady=10)
            self.display_happy()
            self.display_stars(3)
            time.sleep(2)
            self.canvas.destroy()
        elif 3 <= retry_count < 7:
            self.label = tk.Label(self.root, text=f"Almost there, {player_name}!", font=("Poppins", 15))
            self.label.pack(padx=10, pady=10)
            self.display_neutral()
            self.display_stars(2)
            time.sleep(2)
            self.canvas.destroy()
        elif retry_count >= 7:
            self.label = tk.Label(self.root, text=f"Try harder, {player_name}!", font=("Poppins", 15))
            self.label.pack(padx=10, pady=10)
            self.display_sad()
            self.display_stars(1)
            time.sleep(2)
            self.canvas.destroy()

        self.label2 = tk.Label(self.root,text=f"You have learnt {len(learnt_words)} words",font=("Poppins",10))
        self.label2.pack(padx=5,pady=5)

        self.scrollbox = tk.Listbox(self.root)
        # Converts learnt words (list of dictionaries) into the form of ("Chinese Word"),"English Word",
        # seperated by line
        self.simplify_list(learnt_words)
        self.scrollbox.pack(padx=10,pady=10,fill=tk.BOTH,expand=True)

        self.scrollbar = tk.Scrollbar(self.scrollbox)
        self.scrollbar.pack(side=tk.RIGHT)
        self.scrollbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.scrollbox.yview)

        self.label3 = tk.Label(self.root,text=f"Retry Count: {retry_count}",font=("Poppins",10))
        self.label3.pack(padx=5,pady=5)

        self.label4 = tk.Label(self.root, text=f"Time Taken: {time_lapsed}", font=("Poppins", 10))
        self.label4.pack(padx=5, pady=5)

        self.Exit_Button = tk.Button(self.root,text="Exit", font=("Poppins", 16), command=self.exit_to_Main_Menu)
        self.Exit_Button.pack(padx=5,pady=5)

    #Exit to Main Menu, restores learnt_words to an empty list, and dictionary with its original elements for multiple replays
    def exit_to_Main_Menu(self):
        self.root.withdraw()
        Main_Menu_Screen()
        global learnt_words
        learnt_words = []
        global test_dict
        test_dict = test_dict_original.copy()
        global retry_count
        retry_count = 0

    def simplify_list(self,words):
        ls = []
        for i in words:
            a = i["Chinese"], i["English"]
            ls.append(a)
        for values in ls:
            self.scrollbox.insert("end", values)

    def display_happy(self):
        self.face_base()
        t = turtle.RawTurtle(self.canvas)
        t.speed(0.5)
        t.penup()
        t.hideturtle()

        t.color('red')
        t.begin_fill()
        t.setposition(0, 20)
        t.pendown()
        t.circle(50, 90)
        t.left(90)
        t.forward(100)
        t.left(90)
        t.circle(50, 90)
        t.end_fill()

    def display_neutral(self):
        self.face_base()
        t = turtle.RawTurtle(self.canvas)
        t.speed(0.5)
        t.penup()
        t.hideturtle()

        t.setposition(-50, 50)

        t.pendown()
        t.forward(100)
        t.penup()
        t.setposition(0, 20)

    def display_sad(self):
        self.face_base()
        t = turtle.RawTurtle(self.canvas)
        t.penup()
        t.speed(0.5)
        t.hideturtle()

        t.color('red')
        t.begin_fill()
        t.setposition(0,100)
        t.circle(-50, 90)
        t.right(90)
        t.forward(100)
        t.right(90)
        t.circle(-50, 90)
        t.end_fill()

    def face_base(self):
        t = turtle.RawTurtle(self.canvas)
        t.hideturtle()
        t.color('green')
        t.speed(0.5)
        radius = 100
        extent = 360

        t.color('yellow')
        t.begin_fill()
        t.circle(radius, extent)  ##main circle
        t.end_fill()

        t.penup()
        t.setposition(-50, 100)
        t.pendown()
        radius = 25
        extent = 360

        t.color('white')
        t.begin_fill()
        t.circle(radius, extent)  ##first eye
        t.end_fill()

        t.penup()
        t.setposition(50, 100)
        t.pendown()
        radius = 25
        extent = 360

        t.begin_fill()
        t.circle(radius, extent)
        t.end_fill()  ##second eye
        t.penup()

        t.color('black') ##first eye iris
        t.begin_fill()
        t.penup()
        t.setposition(-50, 110)
        t.pendown()
        radius = 12.5
        extent = 360
        t.circle(radius, extent)
        t.end_fill()
        t.penup()

        t.color('black') ##second eye iris
        t.begin_fill()
        t.penup()
        t.setposition(50, 110)
        t.pendown()
        radius = 12.5
        extent = 360
        t.circle(radius, extent)
        t.end_fill()
        t.penup()

    def display_stars(self,stars):
        t = turtle.RawTurtle(self.canvas)
        t.hideturtle()
        t.speed(0.5)
        for k in range(stars):
            t.color('pink')
            t.begin_fill()
            t.penup()
            t.setposition(-100 + 100 * k, -80 - 10 * k)
            t.pendown()
            t.left(60)

            for i in range(5):
                t.forward(30)
                t.right(120)
                t.forward(30)
                t.left(45)
            t.penup()
            t.setposition(-100 + 100 * k, -80 - 10 * k)
            t.end_fill()

class Credits_Screen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Credits")
        self.root.geometry("400x400")

        self.Title_label = tk.Label(self.root, text="2022 10.014 \nComputational Thinking for Design",
                                    font=("Poppins",12))
        self.Title_label.pack(padx=10,pady=10)

        self.Member1_label = tk.Label(self.root, text="1006874 Peh Cheng Ye", font=("Poppins", 12))
        self.Member1_label.pack(padx=10, pady=10)

        self.Member2_label = tk.Label(self.root, text="1006864 Tan Yan Zu, Joe",
                                    font=("Poppins", 12))
        self.Member2_label.pack(padx=10, pady=10)

        self.Member3_label = tk.Label(self.root, text="1007009 Thirunavukkarasu Harshini",
                                    font=("Poppins", 12))
        self.Member3_label.pack(padx=10, pady=10)

        self.Member4_label = tk.Label(self.root, text="1007008 Rout Bishmit",
                                    font=("Poppins", 12))
        self.Member4_label.pack(padx=10, pady=10)

        self.Member5_label = tk.Label(self.root, text="1006867 Neo Yau Jun Lucius",
                                      font=("Poppins", 12))
        self.Member5_label.pack(padx=10, pady=10)

        self.Close_Button = tk.Button(self.root, text="Exit", font=("Poppins", 10), command=self.root.destroy)
        self.Close_Button.pack(padx=10, pady=10)

Start_Screen()



