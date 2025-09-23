from tkinter import *
from tkinter.ttk import Combobox, Button
import math


def choose_func():
    if chosen.get() in [i for i in dir(math) if '_' not in i]:
        if isinstance(eval(chosen.get(), {"__builtins__": None},
                           {i: getattr(math, i) for i in dir(math) if '_' not in i}), float):
            res.set(res.get() + chosen.get())
        else:
            res.set(res.get() + chosen.get() + "(")
    chosen.set("Other...")
    trig.set("Trigonometry")
    root.after(1, lambda: chosen.set("Other..."))


def eq():
    try:
        res.set(res.get() + "=" + str(eval(res.get(), {"__builtins__": None},
                                           {i: getattr(math, i) for i in dir(math) if '_' not in i})))
    except Exception as e:
        res.set(f"{type(e).__name__}: {e}")
    root.bind_all("<Button-1>", lambda _: (res.set(""), root.unbind_all("<Button-1>")))


root = Tk()
root.title("Calculator")
root.resizable(0, 0)

res = StringVar(value="")
Entry(textvariable=res, state="disabled").grid(row=0, column=0, columnspan=5, sticky="nesw")

chosen = StringVar(value="Other...")
chosen.trace_add("write", lambda a, b, c: choose_func())
Combobox(values=[i for i in dir(math) if '_' not in i], textvariable=chosen).grid(row=1, column=2, columnspan=2,
                                                                                  sticky="nesw")
trig = StringVar(value="Trigonometry")
trig.trace_add("write", lambda a, b, c: chosen.set(trig.get()) if trig.get() != "Trigonometry" else None)
Combobox(values=["sin", "cos", "tan", "hypot", "asin", "acos", "atan"],
         textvariable=trig).grid(row=1, column=0, columnspan=2, sticky="nesw")
Button(text="2nd", command=lambda: None).grid(row=2, column=0, sticky="nesw")
Button(text="π", command=lambda: res.set(res.get() + "pi")).grid(row=2, column=1, sticky="nesw")
Button(text="e", command=lambda: res.set(res.get() + "e")).grid(row=2, column=2, sticky="nesw")
Button(text="C", command=lambda: res.set("")).grid(row=2, column=3, sticky="nesw")
Button(text="⇦", command=lambda: res.set(res.get()[:-1])).grid(row=2, column=4, sticky="nesw")
Button(text="x²", command=lambda: res.set(res.get() + "**2")).grid(row=3, column=0, sticky="nesw")
Button(text="⅟x", command=lambda: res.set(res.get() + "(1/")).grid(row=3, column=1, sticky="nesw")
Button(text="|x|", command=lambda: res.set(res.get() + "abs(")).grid(row=3, column=2, sticky="nesw")
Button(text="exp", command=lambda: res.set(res.get() + "exp(")).grid(row=3, column=3, sticky="nesw")
Button(text="mod", command=lambda: res.set(res.get() + "%")).grid(row=3, column=4, sticky="nesw")
Button(text="√", command=lambda: res.set(res.get() + "sqrt(")).grid(row=4, column=0, sticky="nesw")
Button(text="(", command=lambda: res.set(res.get() + "(")).grid(row=4, column=1, sticky="nesw")
Button(text=")", command=lambda: res.set(res.get() + ")")).grid(row=4, column=2, sticky="nesw")
Button(text="n!", command=lambda: res.set(res.get() + "factorial(")).grid(row=4, column=3, sticky="nesw")
Button(text=":", command=lambda: res.set(res.get() + "/")).grid(row=4, column=4, sticky="nesw")
Button(text="xⁿ", command=lambda: res.set(res.get() + "**")).grid(row=5, column=0, sticky="nesw")
Button(text="1", command=lambda: res.set(res.get() + "1")).grid(row=5, column=1, sticky="nesw")
Button(text="2", command=lambda: res.set(res.get() + "2")).grid(row=5, column=2, sticky="nesw")
Button(text="3", command=lambda: res.set(res.get() + "3")).grid(row=5, column=3, sticky="nesw")
Button(text="*", command=lambda: res.set(res.get() + "*")).grid(row=5, column=4, sticky="nesw")
Button(text="10ⁿ", command=lambda: res.set(res.get() + "10**")).grid(row=6, column=0, sticky="nesw")
Button(text="4", command=lambda: res.set(res.get() + "4")).grid(row=6, column=1, sticky="nesw")
Button(text="5", command=lambda: res.set(res.get() + "5")).grid(row=6, column=2, sticky="nesw")
Button(text="6", command=lambda: res.set(res.get() + "6")).grid(row=6, column=3, sticky="nesw")
Button(text="-", command=lambda: res.set(res.get() + "-")).grid(row=6, column=4, sticky="nesw")
Button(text="log", command=lambda: res.set(res.get() + "log10(")).grid(row=7, column=0, sticky="nesw")
Button(text="7", command=lambda: res.set(res.get() + "7")).grid(row=7, column=1, sticky="nesw")
Button(text="8", command=lambda: res.set(res.get() + "8")).grid(row=7, column=2, sticky="nesw")
Button(text="9", command=lambda: res.set(res.get() + "9")).grid(row=7, column=3, sticky="nesw")
Button(text="+", command=lambda: res.set(res.get() + "+")).grid(row=7, column=4, sticky="nesw")
Button(text="ln", command=lambda: res.set(res.get() + "log(")).grid(row=8, column=0, sticky="nesw")
Button(text=",", command=lambda: res.set(res.get() + ", ")).grid(row=8, column=1, sticky="nesw")
Button(text="0", command=lambda: res.set(res.get() + "0")).grid(row=8, column=2, sticky="nesw")
Button(text=".", command=lambda: res.set(res.get() + ".")).grid(row=8, column=3, sticky="nesw")
Button(text="=", command=eq).grid(row=8, column=4, sticky="nesw")

root.mainloop()
