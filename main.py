"""
Animations: https://sora.chatgpt.com + https://aivideomaker.ai + https://ezgif.com
                                       or https://pixlr.com
Sounds:
    Hungry - https://uppbeat.io + https://mp3cut.net
    Thirsty - https://uppbeat.io + https://mp3cut.net
    Playful - https://zvukogram.com + https://mega-sounds.com + https://mp3cut.net + https://clideo.com
    Pet - https://mega-sounds.com + https://mp3cut.net
    Dirty - https://freepik.com + https://mp3cut.net
    Wc - https://mixkit.co/ + https://mp3cut.net
"""
from tkinter import *
from tkinter.ttk import Button, Progressbar, Radiobutton
from tkinter.messagebox import showinfo, askyesno
from PIL import Image, ImageDraw, ImageTk
import random
import time
import os
import winsound
from typing import Any


def playsound(sound: str):
    """
    Play a sound
    If you are not on Windows, this is the perfect place to change the function
    :param sound: Path to sound
    :return: None
    """
    winsound.PlaySound(sound, winsound.SND_ASYNC)


class Characteristic:
    def __init__(self, line: int, btnname: str, sound: str | None = None, down: float = 0.5, up: float = 10,
                 timeout: int = 500, min_: float = 0, max_: float = 100, less: tuple[str, str] | None = None,
                 more: tuple[str, str] | None = None, animations: dict[int: tuple[Any, int]] | None = None,
                 value: float = 50, row: int = 0, column: int = 0):
        """
        Characteristic
        :param btnname: Button text
        :param sound: Sound to play on button press
        :param down: How much down each tick
        :param up: How much up every press
        :param timeout: How much wait before next press
        :param min_: Critical low
        :param max_: Critical high
        :param less: What to show on critical low
        :param more: What to show on critical high
        :param animations: Animations to play
        :param value: Initial value
        :param row: Grid row
        :param column: Grid column
        """
        self.alive = True
        self.line = line
        self.sound = sound
        self.down = down
        self.up = up
        self.timeout = timeout
        self.min_ = min_
        self.max_ = max_
        if less is None:
            less = ("Your cat ran away!", "Your cat ran away!")
        self.less = less
        if more is None:
            more = ("Your cat ran away!", "Your cat ran away!")
        self.more = more
        if animations is None:
            animations = {}
        self.animations = animations
        self.animation = None
        self.frame = 0
        self.var = DoubleVar(value=value)
        self.progressbar = Progressbar(variable=self.var, orient="vertical")
        self.progressbar.grid(row=row, column=column)
        self.button = Button(text=btnname, command=self.onclick)
        self.button.grid(row=row + 1, column=column)

    def tick(self):
        self.var.set(max(self.var.get() - self.down, 0))
        self.save()
        if not self.alive:
            showinfo(*self.more)
            return False
        elif self.var.get() <= self.min_:
            self.alive = False
            showinfo(*self.less)
            return False
        elif self.var.get() >= self.max_:
            self.alive = False
            showinfo(*self.more)
            return False
        lst = [i for i in self.animations.keys() if self.var.get() <= i]
        if len(lst) == 0:
            self.animation = None
            self.frame = 0
        elif self.animations[min(lst)][0] != self.animation:
            self.animation = self.animations[min(lst)][0]
        if len(lst) > 0:
            if self.frame > 0 or random.randint(1, self.animations[min(lst)][1]) == 1:
                self.frame = (self.frame + 1) % len(self.animation)
            else:
                self.frame = 0
            return self.animation[self.frame]
        return None

    def onclick(self):
        self.var.set(min(self.var.get() + self.up, 100))
        self.save()
        if self.sound is not None:
            playsound(self.sound)
        self.button.config(state="disabled")
        if self.var.get() >= self.max_:
            self.alive = False
            return
        self.button.after(self.timeout, lambda: self.button.config(state="normal"))
        return

    def save(self):
        with open("chars.txt", "r", encoding="utf-8") as f:
            lines = f.read().strip().split("\n")
        with open("chars.txt", "w", encoding="utf-8") as f:
            for i in lines[:self.line]:
                f.write(f"{i}\n")
            f.write(f"{self.var.get()};{time.time()}\n")
            for i in lines[self.line + 1:]:
                f.write(f"{i}\n")


def tick():
    global idle_frame
    if idle_frame > 0 or random.randint(1, idle_chance) == 1:
        idle_frame = (idle_frame + 1) % 20
    else:
        idle_frame = 0
    lbl.config(image=anims["idle"][idle_frame])
    for i in chars:
        res = i.tick()
        if res is False:
            root.destroy()
            os.remove("chars.txt")
            return
        if res is not None:
            lbl.config(image=res)
    root.after(tick_speed, tick)


root = Tk()
root.resizable(0, 0)
root.title("Tamagotchi")
root.geometry("+0+0")
root.attributes('-alpha', 0)
root.iconify()

wnd = Tk()
wnd.overrideredirect(1)
wnd.attributes('-topmost', 1)
wnd.attributes("-transparentcolor", "white")
progress = IntVar(wnd, value=0)
tamagotchi_img = Image.open("tamagotchi.png").convert("RGBA")
ImageDraw.floodfill(tamagotchi_img, (tamagotchi_img.size[0] // 2, tamagotchi_img.size[1] // 2), (240, 240, 240, 255))
tamagotchi_size = 360
tamagotchi_size = (tamagotchi_size, tamagotchi_img.size[1] * tamagotchi_size // tamagotchi_img.size[0])
tamagotchi_img = ImageTk.PhotoImage(
    tamagotchi_img.resize(tamagotchi_size), **{"master": wnd})  # PyCharm raises a warning if I do master=wnd
Label(wnd, image=tamagotchi_img, background="white").place(relwidth=1, relheight=1)
difficulty = StringVar()
if os.path.exists("chars.txt"):
    with open("chars.txt", "r", encoding="utf-8") as chars:
        difficulty.set(chars.read().strip().split("\n")[-1])
    Label(wnd, text=f"While you were away, the cat slept{'\n' * 5}Loading...").pack(
        pady=(tamagotchi_size[1] * 2 / 5, 0))
else:
    difficulty.set("Hard")
    Label(wnd, text=f"New game\n").pack(pady=(tamagotchi_size[1] * 2 / 5, 0))
    difflbl = Label(wnd, text="Difficulty: Hard")
    difflbl.pack()

    def ondiffbtn():
        if difficulty.get() == "Hard":
            difficulty.set("Easy")
            difflbl.config(text="Difficulty: Easy")
            diffbtn.config(text="Switch to Hard")
        else:
            difficulty.set("Hard")
            difflbl.config(text="Difficulty: Hard")
            diffbtn.config(text="Switch to Easy")
    diffbtn = Button(wnd, text="Switch to Easy", command=ondiffbtn)
    diffbtn.pack()
    Label(wnd, text="\nLoading...").pack()
Progressbar(wnd, variable=progress).pack(ipadx=40)
wnd.geometry(f"{tamagotchi_size[0]}x{tamagotchi_size[1]}+{wnd.winfo_screenwidth() // 2 - tamagotchi_size[0] // 2}"
             f"+{wnd.winfo_screenheight() // 2 - tamagotchi_size[1] // 2}")

size = 480

anims = {}
d = {"idle": 52, "hungry": 52, "thirsty": 52, "playful": 27, "pet": 52, "dirty": 52, "wc": 52}
summ = 0
for pair in d.items():
    anims[pair[0]] = []
    for frame in range(1, pair[1]):
        summ += 1
        progress.set(summ * 100 // (sum(d.values()) - len(d)))
        wnd.update()
        anims[pair[0]].append(ImageTk.PhotoImage(Image.open(
            f"{pair[0]}/ezgif-frame-{'0' * (3 - len(str(frame)))}{frame}.png").resize((size, size))))

wnd.destroy()
root.deiconify()
root.attributes('-alpha', 1)
root.attributes('-topmost', 1)
root.update()
root.attributes('-topmost', 0)

lbl = Label(image=anims["idle"][0])
lbl.grid(column=0, row=0, columnspan=6)

if not os.path.exists("chars.txt"):
    open("chars.txt", "w", encoding="utf-8").close()

chars = [Characteristic(0, "Feed", "hungry.wav", 0.1, 50,
                        less=("Your cat ran away", "Your cat ran away because you didn't feed it"), max_=101,
                        animations={49: (anims["hungry"], 10)}, column=0, row=1),
         Characteristic(1, "Give water", "thirsty.wav", 0.1,
                        less=("Your cat ran away", "Your cat ran away because you didn't give it water"),
                        more=("Your cat ran away", "Your cat ran away because you almost drowned it!"),
                        animations={20: (anims["thirsty"], 10)}, column=1, row=1),
         Characteristic(2, "Play", "playful.wav", 0.1, 30,
                        less=("Your cat ran away", "Your cat ran away because you didn't play with it"),
                        more=("Your cat ran away", "Your cat ran away because you played with it too much"),
                        animations={30: (anims["playful"], 5)}, column=2, row=1),
         Characteristic(3, "Pet", "pet.wav", 0.1,
                        less=("Your cat ran away", "Your cat ran away because you didn't pet it"),
                        more=("Your cat ran away", "Your cat ran away because you touched it too much"),
                        animations={30: (anims["pet"], 10)}, column=3, row=1),
         Characteristic(4, "Wash", "dirty.wav", 0.1,
                        less=("Your cat ran away", "Your cat ran away because you didn't wash it"),
                        more=("Your cat ran away", "Your cat ran away because you put it in water too much"),
                        animations={20: (anims["dirty"], 20)}, column=4, row=1),
         Characteristic(5, "Clean litter", "wc.wav", 0.1,
                        less=("Your cat ran away", "Your cat ran away because you didn't clean it's litter box"),
                        max_=101,
                        animations={20: (anims["wc"], 10)}, column=5, row=1)]

sleep = {"Easy": [0.02, 0.02, 0.03, 0.03, 0.01, 0.03], "Hard": [0.2, 0.2, 0.3, 0.3, 0.1, 0.3]}
tick_speed = 100
idle_frame = 0
idle_chance = 50

with open("chars.txt", "r", encoding="utf-8") as file:
    loaded = file.read().strip().split("\n")
if len(loaded) > 1:
    difficulty.set(loaded[-1])
    try:
        for idx in range(len(loaded) - 1):
            chars[idx].var.set(float(loaded[idx].split(";")[0]) - chars[idx].down *
                               ((time.time() - float(loaded[idx].split(";")[1])) * 1000 *
                                sleep[difficulty.get()][idx] / tick_speed))
    except Exception as e:
        if askyesno("Invalid data", f"Invalid data:\n{type(e).__name__}: {e}\nClear the data?"):
            os.remove("chars.txt")
        exit(0)
else:
    for char in chars:
        char.save()
    with open("chars.txt", "a", encoding="utf-8") as file:
        file.write(difficulty.get() + "\n")

root.after(tick_speed, tick)

root.mainloop()
