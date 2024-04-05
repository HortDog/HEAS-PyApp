import tkinter as tk


def on_button_click():
    label.config(text="Button clicked!")

root = tk.Tk()

label = tk.Label(root, text="Hello, World!")
label.pack()

button = tk.Button(root, text="Click me!", command=on_button_click)
button.pack()

root.mainloop()