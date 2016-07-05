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

def __init__(self, master):
        self.folder = ""
        self.file = ""
        self.drawables = []

        # FRAMES
        self.folder_select_frame = Frame(root)
        self.file_select_frame = Frame(root)
        self.checkbutton_frame = Frame(root)
        self.footer_frame = Frame(root)
        self.setup_frames()

        # FOLDER SELECT FRAME
        self.folder_help_text = Label(self.folder_select_frame,
                                      text='Select the parent folder containing all the drawable folders (usually "res")')
        self.folder_name_input = Entry(self.folder_select_frame)
        self.browse_button = Button(self.folder_select_frame, text='Browse', command=self.browse_folder)
        self.select_button = Button(self.folder_select_frame, text='Select', command=self.check_folder)
        self.folder_label = Label(self.folder_select_frame, text='Module Folder')
        self.setup_folder_select_frame()

    def setup_frames(self):
        self.folder_select_frame.pack(fill=X, pady=self.frame_padding, padx=self.frame_padding)
        self.file_select_frame.pack(fill=X, pady=self.frame_padding, padx=self.frame_padding)
        self.checkbutton_frame.pack(fill=X, pady=self.frame_padding, padx=self.frame_padding)
        self.footer_frame.pack(fill=X, pady=self.frame_padding, padx=self.frame_padding)

    def setup_folder_select_frame(self):
        self.folder_help_text.pack()
        self.folder_label.pack(side=LEFT)
        self.folder_name_input.pack(side=LEFT)
        self.browse_button.pack(side=LEFT)
        self.select_button.pack(side=LEFT)

    def browse_folder(self):
        Tk().withdraw()
        self.folder = askdirectory()
        self.folder_name_input.delete(0, END)
        self.folder_name_input.insert(0, self.folder)

    def browse_file(self):
        Tk().withdraw()
        self.file = askopenfilename()
        self.file_name_input.delete(0, END)
        self.file_name_input.insert(0, self.file)

    def check_folder(self):
        folder = self.folder_name_input.get()
        hdpi = folder + "/drawable-hdpi"

        if exists(hdpi) and isdir(hdpi):
            self.drawcheckboxes(hdpi)
        else:
            self.folder_help_text['text'] = 'Selected incorrect folder. Please select again.'

    def check_file(self):
        file = self.file_name_input.get()

        if exists(file) and isfile(file):
            self.checkfromfile(file)
        else:
            self.status2['text'] = 'Selected incorrect file. Please select again.'

root = Tk()
window = Window(root)
root.wm_title("Android Drawable Extractor")
root.mainloop()