from os import listdir
from os.path import isfile, join, exists, isdir
from Tkinter import *
from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename


class MyCheckButton(Checkbutton):
    def __init__(self,*args,**kwargs):
        self.var=kwargs.get('variable',IntVar())
        kwargs['variable']=self.var
        Checkbutton.__init__(self,*args,**kwargs)

    def is_checked(self):
        return self.var.get()

class Window:
    frame_padding = 10

    def __init__(self, master):
        self.folder = ""
        self.file = ""
        self.drawables = []

        # FRAMES
        self.folder_select_frame = Frame(root)
        self.file_select_frame = Frame(root)
        self.checkbutton_frame = Frame(root)
        self.footer_frame = Frame(root)
        self.setupFrames()

    def setupFrames(self):
        self.folder_select_frame.pack(fill=X, pady=self.frame_padding, padx=self.frame_padding)
        self.file_select_frame.pack(fill=X, pady=self.frame_padding, padx=self.frame_padding)
        self.checkbutton_frame.pack(fill=X, pady=self.frame_padding, padx=self.frame_padding)
        self.footer_frame.pack(fill=X, pady=self.frame_padding, padx=self.frame_padding)

root = Tk()
window = Window(root)
root.wm_title("Drawable Extractor")
root.mainloop()