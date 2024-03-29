from os import listdir, makedirs
from os.path import isfile, join, exists, isdir
from shutil import copyfile
from Tkinter import *
from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename


class MyCheckButton(Checkbutton):
    def __init__(self, *args, **kwargs):
        self.var = kwargs.get('variable', IntVar())
        self.text = kwargs.get('text', StringVar())
        kwargs['variable'] = self.var
        kwargs['text'] = self.text
        Checkbutton.__init__(self, *args, **kwargs)

    def is_checked(self):
        return self.var.get()

    def get_text(self):
        return self.text


class Window:
    frame_padding = 10
    view_padding = 15
    drawable_dirs = ['/drawable-mdpi/', '/drawable-hdpi/', '/drawable-xhdpi/', '/drawable-xxhdpi/', '/drawable-xxxhdpi/']

    def __init__(self, master):
        self.folder = ""
        self.file = ""
        self.parent_folder_name = ""
        self.drawables = []
        self.checkbuttons = []

        # FRAMES
        self.folder_select_frame = Frame(root)
        self.file_select_frame = Frame(root)
        self.checkbutton_frame = Frame(root)
        self.footer_frame = Frame(root)
        self.setup_frames()

        # FOLDER SELECT FRAME
        self.folder_help_text = Label(self.folder_select_frame,
                                      text='Select the folder containing all the drawable folders (usually "res")')
        self.folder_name_input = Entry(self.folder_select_frame)
        self.browse_folder_button = Button(self.folder_select_frame, text='Browse', command=self.browse_folder)
        self.select_button = Button(self.folder_select_frame, text='Select', command=self.check_folder)
        self.folder_label = Label(self.folder_select_frame, text='Parent Folder')
        self.setup_folder_select_frame()

        # FILE SELECT FRAME
        self.file_helper_text = Label(self.file_select_frame,
                                      text='Select the file containing the names of drawables you wish to export')
        self.file_label = Label(self.file_select_frame, text='Selector File')
        self.file_name_input = Entry(self.file_select_frame)
        self.browse_file_button = Button(self.file_select_frame, text='Browse', command=self.browse_file)
        self.use_file_button = Button(self.file_select_frame, text='Use File', command=self.check_file)

        # CHECKBUTTON FRAME
        self.checkbutton_label = Label(self.checkbutton_frame, text='Select the drawables you wish to export')
        self.vsb = Scrollbar(self.checkbutton_frame, orient='vertical')
        self.text = Text(self.checkbutton_frame, width=40, height=20, yscrollcommand=self.vsb.set)
        self.clear_all = Button(self.checkbutton_frame, text='Clear All', command=self.clear_all)

        # FOOTER FRAME
        self.success_label = Label(self.footer_frame)
        self.output_folder_label = Label(self.footer_frame, text='Output Folder Name')
        self.output_folder_name_input = Entry(self.footer_frame)
        self.extract_button = Button(self.footer_frame, text='Extract Drawables', command=self.extract)

    def setup_frames(self):
        self.folder_select_frame.pack(fill=X, pady=self.frame_padding, padx=self.frame_padding)
        self.file_select_frame.pack(fill=X, pady=self.frame_padding, padx=self.frame_padding)
        self.checkbutton_frame.pack(fill=X)  # padding is in top and bottom child
        self.footer_frame.pack(fill=X, pady=self.frame_padding, padx=self.frame_padding)

    def setup_folder_select_frame(self):
        self.folder_help_text.pack(side=TOP)
        self.folder_label.pack(side=LEFT)
        self.folder_name_input.pack(side=LEFT)
        self.browse_folder_button.pack(side=LEFT)
        self.select_button.pack(side=LEFT)

    def setup_file_selector_frame(self):
        self.file_helper_text.pack(side=TOP)
        self.file_label.pack(side=LEFT)
        self.file_name_input.pack(side=LEFT)
        self.browse_file_button.pack(side=LEFT)
        self.use_file_button.pack(side=LEFT)

    def setup_checkbutton_frame(self):
        self.checkbutton_label.pack(side=TOP, pady=self.view_padding)
        self.clear_all.pack(side=BOTTOM, pady=self.view_padding)
        self.vsb.config(command=self.text.yview)
        self.vsb.pack(side=RIGHT, fill=Y)
        self.text.pack(side=LEFT, fill=BOTH, expand=True)

    def setup_footer_frame(self):
        self.success_label.pack(side=BOTTOM)
        self.output_folder_label.pack(side=LEFT)
        self.output_folder_name_input.pack(side=LEFT)
        self.extract_button.pack(side=LEFT)

    def browse_folder(self):
        self.success_label['text'] = ''
        Tk().withdraw()
        self.folder = askdirectory()
        self.folder_name_input.delete(0, END)
        self.folder_name_input.insert(0, self.folder)

    def browse_file(self):
        self.success_label['text'] = ''
        Tk().withdraw()
        self.file = askopenfilename()
        self.file_name_input.delete(0, END)
        self.file_name_input.insert(0, self.file)

    def check_folder(self):
        folder = self.folder_name_input.get()
        hdpi_folder = folder + '/drawable-hdpi'

        if exists(hdpi_folder) and isdir(hdpi_folder):
            self.setup_file_selector_frame()
            self.setup_checkbutton_frame()
            self.draw_checkboxes(hdpi_folder)
            self.setup_footer_frame()
            self.folder_help_text['text'] = 'Select the folder containing all the drawable folders (usually "res")'
        else:
            self.folder_help_text['text'] = 'Selected incorrect folder. Please select again.'

    def check_file(self):
        filename = self.file_name_input.get()

        if exists(filename) and isfile(filename):
            self.check_from_file(filename)
            self.file_helper_text['text'] = 'Selected incorrect file. Please select again.'
        else:
            self.file_helper_text['text'] = 'Select the file containing the names of drawables you wish to export'

    def draw_checkboxes(self, folder):
        all_files = [f for f in listdir(folder) if isfile(join(folder, f))]

        for i, drawable in enumerate(all_files):
            check = MyCheckButton(self.checkbutton_frame, text=drawable)
            self.checkbuttons.append(check)
            self.drawables.append(drawable.split('.')[0])
            self.text.window_create('end', window=check)
            self.text.insert('end', '\n')  # force one checkbox per line

    def check_from_file(self, filename):
        with open(filename) as f:
            for line in f:
                line = line.replace('\n', '')
                if line in self.drawables:
                    self.checkbuttons[self.drawables.index(line)].select()

    def clear_all(self):
        for c in self.checkbuttons:
            c.deselect()

    def extract(self):
        if self.no_checkbuttons_checked():
            self.success_label['text'] = "Please select at least one drawable you wish to extract."
        elif self.output_folder_name_input.get().strip() == '':
            self.success_label['text'] = "Please select a name for the output folder."
        else:
            output_name = self.folder + '/' + self.output_folder_name_input.get()
            self.create_folders(output_name)
            for i, checkbutton in enumerate(self.checkbuttons):
                if checkbutton.is_checked():
                    self.copy_files(checkbutton.get_text())
            self.success_label['text'] = "Extraction of the selected drawables was successful."

    def no_checkbuttons_checked(self):
        for c in self.checkbuttons:
            if c.is_checked():
                return False
        return True

    def create_folders(self, parent_folder_name):
        self.parent_folder_name = self.create_parent_folder(parent_folder_name)
        for density in self.drawable_dirs:
            makedirs(self.parent_folder_name + density)

    def create_parent_folder(self, folder_name):
        folder_copy_name = folder_name
        copy_number = 1
        while True:
            if not exists(folder_copy_name):
                makedirs(folder_copy_name)
                return folder_copy_name
            else:
                folder_copy_name = folder_name + '_' + str(copy_number)
                copy_number += 1

    def copy_files(self, text):
        for density in self.drawable_dirs:
            if exists(self.folder + density + text):
                copyfile(self.folder + density + text, self.parent_folder_name + density + text)

root = Tk()
window = Window(root)
root.wm_title('Android Drawable Extractor')
root.mainloop()
