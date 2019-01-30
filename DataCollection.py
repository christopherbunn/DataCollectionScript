# Start new image labeling session:
    # Directory for images
    # Directory for description csv
    # Directory for result csv
    # Number of images to show
    # Image breaks

# Information to collect in CSV:
    # Image number
    # Description chosen
    # Amount of time needed to make decision

import tkinter
import tkinter as ttk
import csv
from PIL import ImageTk, Image
from os import listdir
from os.path import isfile, join

class SetParameters:
    def get_params(self):
        def save_parameters(*args):
            self.img_path = img_path_box.get()
            self.desc_path = desc_path_box.get()
            self.res_path= res_path_box.get()
            self.num_img = num_img_box.get()
            self.break_size = break_box.get()
            print(self.img_path)
            window.quit()

        window = tkinter.Tk()
        window.title("Set Experiment Parameters")
        frame = ttk.Frame(window)
        frame.grid(column="0", row="0", sticky=('N', 'W', 'E', 'S'))
        frame.columnconfigure(0,weight=1)
        frame.rowconfigure(0,weight=1)

        field_labels = ["Image Location", "Description Location", "Results Location", "Number of Images", "Break Between Images (seconds)"]

        img_path_box = ttk.StringVar()
        desc_path_box = ttk.StringVar()
        res_path_box = ttk.StringVar()
        num_img_box = ttk.IntVar()
        break_box = ttk.IntVar()

        tkinter.Label(frame, text=field_labels[0]).grid(row=0, column=0, sticky='E')
        img_entry = tkinter.Entry(frame, textvariable=img_path_box)
        img_entry.grid(row=0, column=1,sticky='W')

        tkinter.Label(frame, text=field_labels[1]).grid(row=1, column=0, sticky='E')
        img_entry = tkinter.Entry(frame, textvariable=desc_path_box)
        img_entry.grid(row=1, column=1,sticky='W')

        tkinter.Label(frame, text=field_labels[2]).grid(row=2, column=0, sticky='E')
        img_entry = tkinter.Entry(frame, textvariable=res_path_box)
        img_entry.grid(row=2, column=1,sticky='W')

        tkinter.Label(frame, text=field_labels[3]).grid(row=3, column=0, sticky='E')
        img_entry = tkinter.Entry(frame, textvariable=num_img_box)
        img_entry.grid(row=3, column=1,sticky='W')

        tkinter.Label(frame, text=field_labels[4]).grid(row=4, column=0, sticky='E')
        img_entry = tkinter.Entry(frame, textvariable=break_box)
        img_entry.grid(row=4, column=1,sticky='W')

        tkinter.Button(window, text="Run Experiment", command=save_parameters).grid(row=5)
        window.mainloop()

    def __init__(self):
        self.img_path = ""
        self.desc_path = ""
        self.res_path = ""
        self.num_img = 0
        self.break_size = 0
        # self.get_params()


class RunExperiment:
    def read_image_names(self,params):
        self.image_files = list()
        for file in listdir(params.img_path):
            if isfile(join(params.img_path, file)) and not file.startswith("."):
                self.image_files.append(file)
        self.image_files.sort()
        print(self.image_files)

    def run_trial(self, params, image_name):
        img_frame = ttk.Frame(self.window)
        img_frame.grid(column="0", row="0", sticky=('N', 'W', 'E', 'S'))
        img_frame.columnconfigure(0, weight=1)
        img_frame.rowconfigure(0, weight=1)

        button_frame = ttk.Frame(self.window)
        button_frame.grid(column="0", row="1", sticky=('N', 'W', 'E', 'S'))
        button_frame.columnconfigure(0, weight=1)
        button_frame.rowconfigure(0, weight=1)

        # print(image_name)
        # imgobj = ImageTk.PhotoImage(Image.open(params.img_path + '/' + image_name))
        # ttk.Label(img_frame, image=imgobj).grid(row=0, column=0)

        self.img_canvas = ttk.Canvas(img_frame, width=500, height=500)
        self.img_canvas.grid(row=0, column=0)

        self.img_on_canvas = self.img_canvas.create_image(0, 0, anchor='nw', image=self.my_images[self.my_image_number])

        tkinter.Button(button_frame, text="Top Left", command=self.choose_string).grid(row=1, column=0)
        tkinter.Button(button_frame, text="Top Right", command=self.choose_string).grid(row=1, column=1)
        tkinter.Button(button_frame, text="Bottom Left", command=self.choose_string).grid(row=2, column=0)
        tkinter.Button(button_frame, text="Bottom Right", command=self.choose_string).grid(row=2, column=1)

        self.window.mainloop()

    def choose_string(self):
        print(self.my_image_number)
        if self.my_image_number == (len(self.image_files) - 1):
            self.window.quit()
        else:
            self.my_image_number += 1
            self.img_canvas.itemconfig(self.img_on_canvas, image=self.my_images[self.my_image_number])

    def __init__(self, params):
        self.window = tkinter.Tk()
        self.window.title("Trial 1")
        self.read_image_names(params)
        self.my_images = []
        self.my_image_number = 0
        for image in self.image_files:
            full_path = params.img_path + '/' + image
            print(full_path)
            self.my_images.append(ImageTk.PhotoImage(Image.open(full_path)))
        self.run_trial(params, image)

#Set parameters:
# params = SetParameters()
# print(params.img_path, params.desc_path, params.res_path, params.num_img, params.break_size)

#Run experiment:
params = SetParameters()
params.img_path = 'assets/BenchmarkIMAGES'
RunExperiment(params)

# exp_window = tkinter.Tk()
# exp_window.title("Run Experiment")
# set_param = RunExperiment(exp_window)
# exp_window.mainloop()