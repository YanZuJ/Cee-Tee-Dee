import random
import time as time
import tkinter as tk
from tkinter import messagebox

#global variables
time_lapsed = ""
player_name = ""
current_card = ""
test_dict = [{"Chinese":"Ping Guo","English":"Apple"},
             {"Chinese":"Cheng Zi","English":"Orange"},
             {"Chinese":"Xi Gua","English":"Watermelon"}]
test_dict_copy = test_dict.copy()
learnt_words = []
retry_count = 0

#global functions

#Converts seconds to string statement of hours:minutes:seconds
def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  return f"{int(hours)}:{int(mins)}:{round(sec,2)}"

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

    # You can finally use the enter key to enter your name in the textbox, yeah it sucks
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
        self.root.title("Flashcard 1D")
        self.root.geometry("600x450")

        self.label2 = tk.Label(self.root,text=f"Welcome, {player_name}!",font=("Poppins",15))
        self.label2.pack(padx=5,pady=5)

        self.label = tk.Label(self.root,text= "Flashcards", font=("Poppins", 40, "italic","bold"))
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

## Insert Lucius Code Here

class Gameplay_Screen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gameplay")
        self.root.config(padx=40,pady=40)

        self.canvas = tk.Canvas(self.root, width=800, height=400)
        self.card_title = self.canvas.create_text(400, 150, text="How to Play",font=("Poppins", 40, "italic","bold"))
        self.card_word = self.canvas.create_text(400, 250, text=
        "Reveal- Reveal back of flashcard \n"
        "Correct - Removes flashcard pair from the deck\n"
        "Wrong - Flashcard pair is reshuffled into the deck ", font=("Poppins", 20))
        self.canvas.config(highlightthickness=0)
        self.canvas.grid(row=0,column=0,columnspan=3)

        self.Start_Button = tk.Button(self.root, text="Start Game", font=("Poppins", 20), command=self.start_flashcards)
        self.Start_Button.grid(row=1, column=1)

        # Below Buttons are hidden until start/reveal answer is pressed
        self.Reveal_Button = tk.Button(self.root, text="Reveal", font=("Poppins", 20), command=self.reveal_answer)
        self.Correct_Button = tk.Button(self.root, text="Correct", font=("Poppins", 20),command=self.remove_from_list)
        self.Wrong_Button = tk.Button(self.root, text="Wrong", font=("Poppins", 20,),command=self.test_yourself_again)

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
        self.canvas.itemconfig(self.card_word, text= current_card["English"])
        self.Reveal_Button.grid_forget()
        self.Correct_Button.grid(row=2, column=0)
        self.Wrong_Button.grid(row=2, column=2)

    # Removes current card(dictionary) from dictionary to learn, so player
    # does not get tested again, and appends it to list with words learnt, for player Report
    def remove_from_list(self):
        global current_card
        current_card = random.choice(test_dict)
        self.canvas.itemconfig(self.card_title, text="Chinese")
        self.canvas.itemconfig(self.card_word, text=current_card["Chinese"])
        test_dict.remove(current_card)
        learnt_words.append(current_card)
    # After running out of cards to be tested, timer ends and the Result Screen shows
        if len(test_dict) == 0:
            self.end_time=time.time()
            global time_lapsed
            time_lapsed = self.end_time - self.start_time
            time_lapsed = time_convert(time_lapsed)
            print(time_lapsed)
            Report_Screen()
            self.root.withdraw()
        self.Reveal_Button.grid(row=1, column=1)
        self.Correct_Button.grid_forget()
        self.Wrong_Button.grid_forget()

    #Pressing "Test yourself" increases the counter by 1, for player Report
    def test_yourself_again(self):
        global retry_count
        retry_count += 1
        global current_card
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
        self.root.geometry("400x500")

        self.label = tk.Label(self.root,text=f"{player_name}'s Report", font=("Poppins",30))
        self.label.pack(padx=10,pady=10)

        self.label2 = tk.Label(self.root,text=f"You have learnt {len(learnt_words)} words",font=("Poppins",10))
        self.label2.pack(padx=5,pady=5)

        self.scrollbox = tk.Listbox(self.root)
        for values in learnt_words:
            self.scrollbox.insert("end", values)
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
        global test_dict_copy
        test_dict = test_dict_copy
        global retry_count
        retry_count=0

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

        self.Member5_label = tk.Label(self.root, text="1006867 Neo Yao Jun Lucius",
                                      font=("Poppins", 12))
        self.Member5_label.pack(padx=10, pady=10)

        self.Close_Button = tk.Button(self.root, text="Exit", font=("Poppins", 10), command=self.root.destroy)
        self.Close_Button.pack(padx=10, pady=10)

Start_Screen()


