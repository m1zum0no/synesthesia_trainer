# this class is provided by jakirkpatrick
# from https://jakirkpatrick.wordpress.com/2012/02/01/making-a-hovering-box-in-tkinter/

from tkinter import Menu


class HoverInfo(Menu):
    def __init__(self, parent, text):
        super().__init__(parent, tearoff=0)
        if not isinstance(text, str):
            raise TypeError('Trying to initialise a Hover Menu with a non string type: ' + type(text).__name__)

        for t in text.split('\n'):
            self.add_command(label=t)

        self.master.bind("<Enter>", self.display)
        self.master.bind("<Leave>", self.remove)
    
    def display(self, event):
        x = self.master.winfo_rootx() + self.master.winfo_width() // 5
        y = self.master.winfo_rooty() + self.master.winfo_height() + 2
        self.post(x, y)
    
    def remove(self, event):
        self.unpost()
