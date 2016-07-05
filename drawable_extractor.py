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