import random
import csv
import tkinter as tk
from PIL import ImageTk, Image
import tkinter.messagebox as MessageBox
import sys

class Card():
    def __init__(self, value: int, family: int, face: int) -> None:
        self.value = value
        self.family = family
        self.face = face
        pass

    def __str__(self) -> str:
        return f"{self.value}"

### FACES
### 0 - 8 - number
### 9 - king
### 10 - queen
### 11 - jack
### 12 - ace

### FAMILIES
### 0 - hearts
### 1 - diamonds
### 2 - clubs
### 3 - spades

# 2 3 4 5 6 7 8 9 10
# 0 1 2 3 4 5 6 7 8

class Deck():
    def __init__(self) -> None:
        self.cards = []
        self.fill_deck()

    def shuffle_deck(self) -> None:
        random.shuffle(self.cards)

    def fill_deck(self) -> None:
        self.available_faces = [i for i in range(9)]

        for i in range(9):
            self.cards.append(Card(value=i + 2, family=0, face=self.available_faces[i]))
            self.cards.append(Card(value=i + 2, family=1, face=self.available_faces[i]))
            self.cards.append(Card(value=i + 2, family=2, face=self.available_faces[i]))
            self.cards.append(Card(value=i + 2, family=3, face=self.available_faces[i]))

        self.cards.append(Card(10, 0, 9))
        self.cards.append(Card(10, 1, 9))
        self.cards.append(Card(10, 2, 9))
        self.cards.append(Card(10, 3, 9))
        self.cards.append(Card(10, 0, 10))
        self.cards.append(Card(10, 1, 10))
        self.cards.append(Card(10, 2, 10))
        self.cards.append(Card(10, 3, 10))
        self.cards.append(Card(10, 0, 11))
        self.cards.append(Card(10, 1, 11))
        self.cards.append(Card(10, 2, 11))
        self.cards.append(Card(10, 3, 11))
        self.cards.append(Card(11, 0, 12))
        self.cards.append(Card(11, 1, 12))
        self.cards.append(Card(11, 2, 12))
        self.cards.append(Card(11, 3, 12))
        self.shuffle_deck()

    def pull_card(self) -> Card:
        return self.cards.pop(random.randrange(len(self.cards)))
    
class Shoe():
    def __init__(self, num_of_decks=4) -> None:
        self.deck = Deck()
        for _ in range(num_of_decks - 1):
            d = Deck()
            self.deck.cards.extend(d.cards)
        self.deck.shuffle_deck()

class Dealer():
    def __init__(self) -> None:
        self.hand = Hand()

    def set_hand(self, cards: list) -> None:
        self.hand.set_hand(cards)

    def get_upcard(self) -> Card:
        return self.hand.cards[0]

class Player():
    def __init__(self) -> None:
        self.hand = Hand()

    def set_hand(self, cards: list) -> None:
        self.hand.set_hand(cards)

class Hand():
    def __init__(self) -> None:
        self.cards = []

    def get_total(self) -> tuple:
        total = 0
        set = "HARD"

        if self.cards[0].face == self.cards[1].face and len(self.cards) == 2:
            set = "SPLITS"
            total = self.cards[0].value
        else:
            for c in self.cards:
                if c.value == 11 and len(self.cards) == 2:
                    set = "SOFT"
                total += c.value
        return (total, set)
    
    def set_hand(self, cards: list) -> None:
        self.cards = cards

class Trainer():
    def __init__(self, num_of_decks: int=4) -> None:
        self.shoe = Shoe(num_of_decks)
        self.dealer = Dealer()
        self.player = Player()
        self.current_count = 0
        self.num_of_decks = num_of_decks

    def pull_card(self) -> Card:
        if len(self.shoe.deck.cards) <= 4:
            for _ in range(self.num_of_decks):
                d = Deck()
                self.shoe.deck.cards.extend(d.cards)
            self.shoe.deck.shuffle_deck()
        card = self.shoe.deck.pull_card()
        match card.value:
            case 10:
                self.current_count -= 2
            case 8 | 9 | 11:
                pass
            case 2 | 3 | 6 | 7:
                self.current_count += 1
            case 4 | 5:
                self.current_count += 2
        return card

    def check_move(self, move: str, dealer_upcard: Card, player_hand: Hand) -> tuple[str, bool]:
        total, set = player_hand.get_total()
        upcard = dealer_upcard.value
        with open(f"{set}.csv", mode="r", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            upcard_index = 0
            first_row = next(reader)
            correct_move = ""
            is_move_correct = False

            for i in range(len(first_row)):
                if first_row[i] == str(upcard):
                    upcard_index = i
            for row in reader:
                if row[0] == str(total):
                    correct_move, is_move_correct = (row[upcard_index], move == row[upcard_index])
                    break
            return correct_move, is_move_correct

class GUI():
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Blackjack Trainer")
        self.window.option_add('*Font', ('Verdana', 16))
        self.window.option_add('*Background', "#1d151a")
        self.window.option_add('*Foreground', "#F7EBEB")

        self.mainframe = tk.Frame(self.window)

        self.accuracy_frame = tk.Frame(self.mainframe)

        self.card_info_frame = tk.Frame(self.mainframe)

        self.card_frame = tk.Frame(self.mainframe)

        self.tk_image_upcard = None
        self.tk_image_player_card_1 = None
        self.tk_image_player_card_2 = None
        self.upcard_label = tk.Label(self.card_frame)
        self.image_player_card_1_label = tk.Label(self.card_frame)
        self.image_player_card_2_label = tk.Label(self.card_frame)

        self.guess_box_frame = tk.Frame(self.mainframe)

        self.btn_frame = tk.Frame(self.mainframe)

        self.upcard_label = tk.Label(self.card_frame)
        self.image_player_card_1_label = tk.Label(self.card_frame)
        self.image_player_card_2_label = tk.Label(self.card_frame)

        self.trainer = Trainer(num_of_decks=4)

    def start(self) -> None:

        def deal() -> None:
            self.trainer.dealer.set_hand([self.trainer.pull_card()])
            self.trainer.player.set_hand([self.trainer.pull_card(), self.trainer.pull_card()])
        
        deal()

        games_count = 0
        correct_move_guesses = 0
        accuracy_percent = 0
        current_count_guess = tk.IntVar()
        changed = False

        def update_color() -> None:
            correct_label.configure(bg="#2e6db4", text="")

        def handle_any_btn(move: str) -> None:
            nonlocal correct_move_guesses, accuracy_percent, games_count, changed
            total, set = self.trainer.player.hand.get_total()
            if games_count % 5 == 0 and not changed:
                correct_label.configure(text="Guess current count", fg="#FFFFFF")
                return
            correct_move, is_move_correct = self.trainer.check_move(move, self.trainer.dealer.get_upcard(), self.trainer.player.hand)
            if not is_move_correct:
                with open("mistakes.txt", mode="a+", encoding="utf-8") as f:
                    f.seek(0)
                    lines = f.readlines()
                    target = f"{total, set}"
                    found = False
                    for i, line in enumerate(lines):
                        if target in line:
                            parts = line.rstrip("\n").split()
                            count = int(parts[-1]) + 1
                            parts[-1] = str(count)
                            lines[i] = " ".join(parts) + "\n"
                            found = True
                            break
                    if not found:
                        lines.append(f"{target} 1\n")
                    f.seek(0)
                    f.truncate()
                    f.writelines(lines)
            correct_move_guesses += 1 if is_move_correct else 0
            games_count += 1
            accuracy_percent = correct_move_guesses / games_count
            acc.configure(text=f"Accuracy: {accuracy_percent: .0%}")
            games.configure(text=f"Games: {games_count}")
            correct_label.configure(bg="#00ac9f" if is_move_correct else "#df0024", text=f"Wrong! You should {correct_move}" if not is_move_correct else "")
            self.window.after(1000, update_color)
            changed = False
            deal()

        def handle_hit_btn(event) -> None:
            handle_any_btn("HIT")

        def handle_stand_btn(event) -> None:
            handle_any_btn("STAND")

        def handle_double_btn(event) -> None:
            handle_any_btn("DOUBLE")

        def handle_split_btn(event) -> None:
            handle_any_btn("SPLIT")

        def handle_guess_box_enter(event) -> None:
            if event.keysym == "Return":
                nonlocal current_count_guess, changed
                try:
                    correct_label.configure(bg="#00ac9f" if current_count_guess.get() == self.trainer.current_count else "#df0024", text=f"Wrong! The count is {self.trainer.current_count}" if current_count_guess.get() != self.trainer.current_count else "")
                except tk.TclError as e:
                    correct_label.configure(bg="#df0024", text="Enter a valid integer")
                    self.window.after(800, update_color)
                    return
                real_current_count.configure(text=f"Last current count: {self.trainer.current_count}")
                changed = True
                current_count_guess.set(0)
                self.window.after(800, update_color)

        upcard_label = tk.Label(self.card_info_frame, text="Upcard")
        player_hand_label = tk.Label(self.card_info_frame, text="Your Hand")
        self.card_info_frame.place(relx=0.5, y=60, height=60, width=1200, anchor="n")
        upcard_label.place(x=0, y=0, height=60, width=360)
        player_hand_label.place(x=445, y=0, height=60, width=755)

        self.card_frame.place(relx=0.5, y=60+60, height=540, width=1200, anchor="n")
        
        self.guess_box_frame.place(relx=0.5, y=690, height=60, width=640, anchor="n")
        guess_label = tk.Label(self.guess_box_frame, text="Guess current count:", font=("Verdana", 11))
        guess_input = tk.Entry(self.guess_box_frame, textvariable=current_count_guess, state="normal")
        real_current_count = tk.Label(self.guess_box_frame, text="Current count: ?", font=("Verdana", 11))
        guess_label.place(x=0, y=0, height=60, width=200)
        guess_input.place(x=220, y=0, height=60, width=200)
        real_current_count.place(x=440, y=0, height=60, width=200)

        hit_btn = tk.Button(self.btn_frame, text="HIT", bg="#f53955", border=0)
        stand_btn = tk.Button(self.btn_frame, text="STAND", bg="#39ccf5", border=0)
        double_btn = tk.Button(self.btn_frame, text="DOUBLE", bg="#5cf539", border=0)
        split_btn = tk.Button(self.btn_frame, text="SPLIT", bg="#bd39f5", border=0)
        self.btn_frame.place(relx=0.5, y=690+90, height=60, width=860, anchor="n")
        hit_btn.place(x=0, y=0, height=60, width=200)
        stand_btn.place(x=220, y=0, height=60, width=200)
        double_btn.place(x=440, y=0, height=60, width=200)
        split_btn.place(x=660, y=0, height=60, width=200)

        correct_label = tk.Label(self.mainframe, bg="#2e6db4")
        correct_label.place(relx=0.5, y=690+90+90, height=60, width=860, anchor="n")

        acc = tk.Label(self.accuracy_frame, text=f"Accuracy: {accuracy_percent: .0%}")
        games = tk.Label(self.accuracy_frame, text=f"Games: {games_count}")
        self.accuracy_frame.place(relx=0.5, y=690+270, height=60, width=695, anchor="n")
        acc.place(x=0, y=0, height=60, width=200)
        games.place(x=495, y=0, height=60, width=200)

        assets_path = ".\\assets\\" if sys.platform == "win32" else "./assets/"

        def update_images() -> None:
            if games_count % 5 == 0 and not changed:
                correct_label.configure(text="Guess current count", fg="#FFFFFF")
                guess_input.configure(state="normal")
            else:
                guess_input.configure(state="disabled")
            image_upcard = Image.open(f"{assets_path}{self.trainer.dealer.get_upcard().face}_{self.trainer.dealer.get_upcard().family}.png")
            self.tk_image_upcard = ImageTk.PhotoImage(image_upcard)
            image_player_card_1 = Image.open(f"{assets_path}{self.trainer.player.hand.cards[0].face}_{self.trainer.player.hand.cards[0].family}.png")
            self.tk_image_player_card_1 = ImageTk.PhotoImage(image_player_card_1)
            image_player_card_2 = Image.open(f"{assets_path}{self.trainer.player.hand.cards[1].face}_{self.trainer.player.hand.cards[1].family}.png")
            self.tk_image_player_card_2 = ImageTk.PhotoImage(image_player_card_2)

            self.upcard_label.config(image=self.tk_image_upcard)
            self.image_player_card_1_label.config(image=self.tk_image_player_card_1)
            self.image_player_card_2_label.config(image=self.tk_image_player_card_2)

            self.window.after(1000, update_images) 

        self.upcard_label.place(x=0, y=0, height=540, width=360)
        self.image_player_card_1_label.place(x=445, y=0, height=540, width=360)
        self.image_player_card_2_label.place(x=840, y=0, height=540, width=360)

        update_images()

        guess_input.bind("<KeyPress>", handle_guess_box_enter)

        hit_btn.bind("<Button-1>", handle_hit_btn)
        stand_btn.bind("<Button-1>", handle_stand_btn)
        double_btn.bind("<Button-1>", handle_double_btn)
        split_btn.bind("<Button-1>", handle_split_btn)

        self.mainframe.pack(expand=True, side=tk.TOP, fill=tk.BOTH)

        MessageBox.showinfo("Trainer", "You will be asked every 5 games to guess the current count. The count is calculated with Hi-opt II strategy. Your moves will be compared with basic strategy.")

        self.window.mainloop()
