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
from tkinter.ttk import Button, Progressbar
from tkinter.messagebox import showinfo, askyesno
from PIL import Image, ImageFile, ImageDraw, ImageTk
import random
import time
import math
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
    def __init__(self, line: int, sound: str | None = None, down: float = 0.5, up: float = 10,
                 timeout: int = 500, min_: float = 0, max_: float = 100, less: tuple[str, str] | None = None,
                 more: tuple[str, str] | None = None, animations: dict[int: tuple[Any, int]] | None = None,
                 value: float = 50, onclick_image: Any = None, x: int = 0, y: int = 0, radius: int = 25):
        """
        Characteristic
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
        :param onclick_image: Image to show on click
        :param x: Button place x
        :param y: Button place y
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
        self.radius = radius
        self.onclick_image = onclick_image.resize((self.radius * 2, self.radius * 2))
        self.clicked = BooleanVar(value=False)
        self.x = x
        self.y = y
        self.var = DoubleVar(value=value)
        # self.progressbar = Progressbar(variable=self.var, orient="vertical")
        # self.progressbar.place(x=x, y=y)

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
            return self.animation[self.frame].copy()
        return None

    def onclick(self, event: Event) -> None:
        """
        Handles clicking
        :param event: click event
        :return: None
        """
        if self.clicked.get() is True or math.hypot(abs(event.x - self.x), abs(event.y - self.y)) > self.radius:
            return
        self.var.set(min(self.var.get() + self.up, 100))
        self.save()
        if self.sound is not None:
            playsound(self.sound)
        # label = Label(image=self.onclick_image, background="#000000")
        # label.place(x=self.x - self.radius, y=self.y - self.radius)
        self.clicked.set(True)
        root.after(self.timeout, lambda: self.clicked.set(False))
        if self.var.get() >= self.max_:
            self.alive = False
            return
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
    img = anims["idle"][idle_frame].copy()
    clicked = []
    # lbl.config(image=img)
    for i in chars:
        res: bool | None | ImageFile.ImageFile = i.tick()
        if res is False:
            root.destroy()
            os.remove("chars.txt")
            return
        if i.clicked.get():
            clicked.append((i.onclick_image, i.x - i.radius, i.y - i.radius))
        if res is not None:
            img = res
    root.after(tick_speed, tick)
    for i in clicked:
        img.paste(i[0], (i[1], i[2]), i[0])
    img = ImageTk.PhotoImage(img)
    lbl.config(image=img)
    lbl.image = img


def onclick(event, do_chars=True):
    if do_chars:
        for i in chars:
            i.onclick(event)
    if math.hypot(abs(event.x - 243), abs(event.y - 82)) <= 25:
        root.destroy()
        exit(0)


root = Tk()
root.title("Tamagotchi")
root.overrideredirect(1)
root.attributes('-topmost', 1)
root.attributes("-transparentcolor", "white")
root.bind_all("<Button-1>", lambda ev: onclick(ev, False))
progress = IntVar(value=0)
tamagotchi_image = Image.open("tamagotchi.png").convert("RGBA")
tamagotchi_img = tamagotchi_image.copy()
ImageDraw.floodfill(tamagotchi_img, (tamagotchi_img.size[0] // 2, tamagotchi_img.size[1] // 2),
                    (240, 240, 240, 255))
tamagotchi_size = 480
tamagotchi_size = (tamagotchi_size, tamagotchi_img.size[1] * tamagotchi_size // tamagotchi_img.size[0])
tamagotchi_img = ImageTk.PhotoImage(tamagotchi_img.resize(tamagotchi_size))
lbl = Label(image=tamagotchi_img, background="white")
lbl.place(relwidth=1, relheight=1)
difficulty = StringVar()
if os.path.exists("chars.txt"):
    with open("chars.txt", "r", encoding="utf-8") as file:
        difficulty.set(file.read().strip().split("\n")[-1])
    infolbl = Label(text=f"While you were away, the cat slept{'\n' * 5}Loading...")
    infolbl.pack(pady=(tamagotchi_size[1] * 2 / 5, 0))
else:
    difficulty.set("Hard")
    infolbl = Label(text=f"New game\n")
    infolbl.pack(pady=(tamagotchi_size[1] * 2 / 5, 0))
    difflbl = Label(text="Difficulty: Hard")
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
    diffbtn = Button(text="Switch to Easy", command=ondiffbtn)
    diffbtn.pack()
    loadlbl = Label(text="\nLoading...")
    loadlbl.pack()
pb = Progressbar(variable=progress)
pb.pack(ipadx=40)
root.geometry(f"{tamagotchi_size[0]}x{tamagotchi_size[1]}+{root.winfo_screenwidth() // 2 - tamagotchi_size[0] // 2}"
              f"+{root.winfo_screenheight() // 2 - tamagotchi_size[1] // 2}")

tamagotchi_size = 480
size = 374
pos = (164, 308 - 20)

# buttons = []
# for i in range(1, 7):
#     im = Image.open(f"button_{i}.png").convert("RGBA")
#     buttons.append(ImageTk.PhotoImage(im.resize((tamagotchi_size * im.size[0] // im.size[1], tamagotchi_size))))

anims = {}
d = {"idle": 52, "hungry": 52, "thirsty": 52, "playful": 27, "pet": 52, "dirty": 52, "wc": 52}
summ = 0
for pair in d.items():
    anims[pair[0]] = []
    for frame in range(1, pair[1]):
        summ += 1
        progress.set(summ * 100 // (sum(d.values()) - len(d)))
        root.update()
        im = tamagotchi_image.copy()
        im.paste(Image.open(f"{pair[0]}/ezgif-frame-{'0' * (3 - len(str(frame)))}{frame}.png").convert("RGBA").resize((
                size, size)), pos)
        im.paste(tamagotchi_image, (0, 0), tamagotchi_image)
        im = im.resize((tamagotchi_size, tamagotchi_size * im.size[1] // im.size[0]))
        anims[pair[0]].append(im)

pb.destroy()
infolbl.destroy()
if not os.path.exists("chars.txt"):
    # noinspection PyUnboundLocalVariable
    difflbl.destroy()
    # noinspection PyUnboundLocalVariable
    diffbtn.destroy()
    # noinspection PyUnboundLocalVariable
    loadlbl.destroy()

if not os.path.exists("chars.txt"):
    open("chars.txt", "w", encoding="utf-8").close()

btnimg = Image.open("button.png")

chars = [Characteristic(0, "hungry.wav", 0.1, 50,
                        less=("Your cat ran away", "Your cat ran away because you didn't feed it"), max_=101,
                        animations={49: (anims["hungry"], 10)}, onclick_image=btnimg, x=104, y=491),
         Characteristic(1, "thirsty.wav", 0.1,
                        less=("Your cat ran away", "Your cat ran away because you didn't give it water"),
                        more=("Your cat ran away", "Your cat ran away because you almost drowned it!"),
                        animations={20: (anims["thirsty"], 10)}, onclick_image=btnimg, x=159, y=509),
         Characteristic(2, "playful.wav", 0.1, 30,
                        less=("Your cat ran away", "Your cat ran away because you didn't play with it"),
                        more=("Your cat ran away", "Your cat ran away because you played with it too much"),
                        animations={30: (anims["playful"], 5)}, onclick_image=btnimg, x=212, y=519),
         Characteristic(3, "pet.wav", 0.1,
                        less=("Your cat ran away", "Your cat ran away because you didn't pet it"),
                        more=("Your cat ran away", "Your cat ran away because you touched it too much"),
                        animations={30: (anims["pet"], 10)}, onclick_image=btnimg, x=265, y=519),
         Characteristic(4, "dirty.wav", 0.1,
                        less=("Your cat ran away", "Your cat ran away because you didn't wash it"),
                        more=("Your cat ran away", "Your cat ran away because you put it in water too much"),
                        animations={20: (anims["dirty"], 20)}, onclick_image=btnimg, x=320, y=512),
         Characteristic(5, "wc.wav", 0.1,
                        less=("Your cat ran away", "Your cat ran away because you didn't clean it's litter box"),
                        max_=101,
                        animations={20: (anims["wc"], 10)}, onclick_image=btnimg, x=374, y=492)]

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

root.unbind_all("<Button-1>")
root.bind_all("<Button-1>", onclick)

root.after(tick_speed, tick)

root.mainloop()
