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
import random
import time
from functools import partial
from PIL import ImageTk, Image
from os import listdir, path
from os.path import isfile, join
import os


def beep():
    duration = 0.35  # second
    freq = 240  # Hz
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))


def left_beep():
    duration = 0.5  # second
    freq = 640  # Hz
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
    time.sleep(1)
    os.system('say next image')


def right_beep():
    duration = 0.5  # second
    freq = 540  # Hz
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
    time.sleep(1)
    os.system('say next image')


class Entry:
    image_name = ""
    choice = ""
    alternate = ""
    choice_pos = ""
    duration = 0.0
    run_type = "" #trial, control1, control2
    num_repeats = ""


class SetParameters:
    def get_params(self):
        def save_parameters(*args):
            self.img_path = img_path_box.get()
            self.desc_path = desc_path_box.get()
            self.res_path= res_path_box.get()
            # self.num_img = num_img_box.get()
            # self.break_size = break_box.get()
            print(self.img_path)
            window.destroy()

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
        img_entry.insert(0,'assets/BenchmarkIMAGES')
        img_entry.grid(row=0, column=1,sticky='W')

        tkinter.Label(frame, text=field_labels[1]).grid(row=1, column=0, sticky='E')
        desc_entry = tkinter.Entry(frame, textvariable=desc_path_box)
        desc_entry.insert(0, 'assets/descriptions.csv')
        desc_entry.grid(row=1, column=1,sticky='W')

        tkinter.Label(frame, text=field_labels[2]).grid(row=2, column=0, sticky='E')
        res_entry = tkinter.Entry(frame, textvariable=res_path_box)
        res_entry.insert(0, 'results.csv')
        res_entry.grid(row=2, column=1,sticky='W')

        # tkinter.Label(frame, text=field_labels[3]).grid(row=3, column=0, sticky='E')
        # num_img_entry = tkinter.Entry(frame, textvariable=num_img_box)
        # num_img_entry.grid(row=3, column=1,sticky='W')
        #
        # tkinter.Label(frame, text=field_labels[4]).grid(row=4, column=0, sticky='E')
        # break_entry = tkinter.Entry(frame, textvariable=break_box)
        # break_entry.grid(row=4, column=1,sticky='W')

        tkinter.Button(window, text="Run Experiment", command=save_parameters).grid(row=5)
        window.mainloop()

    def __init__(self):
        self.img_path = 'assets/BenchmarkIMAGES'
        self.desc_path = 'assets/descriptions.csv'
        self.res_path = 'results.csv'
        self.num_img = 0
        self.break_size = 0
        self.get_params()


class ReadInstructions:
    def read_instructions(self):
        os.system('say "' + 'A series of photos will be shown. Each photo will have two captions associated '
                            'with the photo. Before each caption is read, this tone will sound. "')
        time.sleep(0.25)
        beep()
        time.sleep(0.25)
        os.system('say "' + 'Each caption will be denoted with left or right at the beginning. '
                            'If the left caption fits the best, press the q key. If the right caption fits the best,'
                            'press the p key. To repeat both captions, press the space bar. To begin the experiment,'
                            'press the space bar."')

    def exit_window(self, event):
        self.window.destroy()

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Read Instructions")
        label = ttk.Label(self.window, text="SPEAKING INSTRUCTIONS, PRESS SPACE TO CONTINUE")
        label.pack()
        self.window.bind("<space>", self.exit_window)
        self.window.tkraise()
        self.window.update()
        self.read_instructions()
        self.window.mainloop()


class RunExperiment:
    def read_image_names(self,params):
        self.image_files = list()
        for file in listdir(params.img_path):
            if isfile(join(params.img_path, file)) and not file.startswith("."):
                self.image_files.append(file)
        self.image_files.sort()
        print(self.image_files)

    def get_labels(self, image):
        all_labels = self.descriptions[image]
        chosen_labels = []
        while len(chosen_labels) < 4:
            idx = random.randint(0,len(all_labels) - 1)
            if all_labels[idx] not in chosen_labels:
                chosen_labels.append(all_labels[idx])
        for label_l in chosen_labels:
            for label_r in chosen_labels:
                if label_l != label_r and (image, label_r, label_l) not in self.label_pairs:
                    self.label_pairs.add((image, label_l, label_r, "Trial"))

    def get_nonsense_list(self, num_of_nonsense):
        nonsense = ["TEST TEST 1", "TEST TEST 2", "TEST TEST 3"] # Insert reading nonsense
        final_list = []
        while len(final_list) < num_of_nonsense:
            final_list.append(random.choice(nonsense))
        return final_list

    def add_control_cases(self):
        rev_pairs = []
        nonsense_pairs = []
        # Reverse pair - 10% - Control 1
        num_rev_pairs = len(self.label_pairs) * 0.1
        while len(rev_pairs) < num_rev_pairs:
            old_pair = self.label_pairs.pop()
            new_pair = (old_pair[0],old_pair[2], old_pair[1], "Reverse Control")
            rev_pairs.append(new_pair)
            self.label_pairs.add(old_pair)
        # Nonsense pair - 5% - Control 2
        num_nonsense_pairs = len(self.label_pairs) * 0.05
        new_labels = self.get_nonsense_list(num_nonsense_pairs)
        left_nonsense_pair = num_nonsense_pairs / 2
        right_nonsense_pair = num_nonsense_pairs - left_nonsense_pair
        while len(nonsense_pairs) < num_nonsense_pairs:
            old_pair = self.label_pairs.pop()
            if left_nonsense_pair > 0: # Left
                new_pair = (old_pair[0], random.choice(new_labels), old_pair[2], "Nonsense Control - Left")
                left_nonsense_pair -= 1
            else: #Right
                old_pair = self.label_pairs.pop()
                new_pair = (old_pair[0], old_pair[1], random.choice(new_labels), "Nonsense Control - Right")
                right_nonsense_pair -= 1
            nonsense_pairs.append(new_pair)
            self.label_pairs.add(old_pair)
        for new_pairs in rev_pairs:
            self.label_pairs.add(new_pairs)
        for new_pairs in nonsense_pairs:
            self.label_pairs.add(new_pairs)


    def read_label(self, event=None):
        beep()
        time.sleep(0.6)
        os.system('say ' + 'left: ' + self.left_label.replace('\'', '\\\''))
        time.sleep(1)
        beep()
        time.sleep(0.6)
        os.system('say ' + 'right: ' + self.right_label.replace('\'', '\\\''))


    def repeat_label(self, event=None):
        self.repeat_counter += 1
        self.read_label()

    def run_trial(self, params):
        img_frame = ttk.Frame(self.window)
        img_frame.pack()

        button_frame = ttk.Frame(self.window)
        button_frame.pack()

        curr_label_pair = self.label_pairs.pop()
        self.curr_image_name = curr_label_pair[0]
        self.left_label = curr_label_pair[1]
        self.right_label = curr_label_pair[2]
        self.run_type = curr_label_pair[3]

        self.img_canvas = ttk.Canvas(img_frame, width=self.my_images[self.curr_image_name].width(), height=self.my_images[self.curr_image_name].height())
        self.img_canvas.pack()
        self.repeat_counter = 0
        self.img_on_canvas = self.img_canvas.create_image(0, 0, anchor='nw', image=self.my_images[self.curr_image_name])

        font = "Courier"
        font_size = 30
        top_left_act = partial(self.choose_string, self.curr_image_name, 'left', params.res_path)
        self.top_left_bttn = tkinter.Button(button_frame, text=self.left_label, command=top_left_act, font=(font, font_size))
        self.top_left_bttn.pack()
        self.window.bind("q",top_left_act)

        top_right_act = partial(self.choose_string, self.curr_image_name, 'right', params.res_path)
        self.top_right_bttn = tkinter.Button(button_frame, text=self.right_label, command=top_right_act, font=(font, font_size))
        self.top_right_bttn.pack()
        self.window.bind("p",top_right_act)
        self.window.bind("<space>", self.repeat_label)
        self.window.tkraise()
        self.window.update()
        self.read_label()
        self.start_time = time.time()
        self.window.mainloop()

    def choose_string(self, img_name, pressed, res_path, event=None):
        self.end_time = time.time()
        if pressed == 'left':
            left_beep()
            choice = self.top_left_bttn['text']
            alternative = self.top_right_bttn['text']
        else:
            right_beep()
            choice = self.top_right_bttn['text']
            alternative = self.top_left_bttn['text']
        self.write_entry(res_path, self.curr_image_name, choice, alternative)
        if len(self.label_pairs) == 0:
            self.window.destroy()
        else:
            self.repeat_counter = 0
            curr_label_pair = self.label_pairs.pop();
            self.curr_image_name = curr_label_pair[0]
            self.left_label = curr_label_pair[1]
            self.right_label = curr_label_pair[2]
            self.img_canvas.itemconfig(self.img_on_canvas, image=self.my_images[self.curr_image_name])
            self.top_left_bttn.configure(text=self.left_label)
            self.top_right_bttn.configure(text=self.right_label)
            self.window.update()
            self.read_label()
            self.start_time = time.time()

    def write_entry(self, res_path, img_name, choice, alternative):
        if path.isfile(res_path) is not True:
            with open(res_path, 'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='\"', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(['Image name', 'Choice', 'Alternative', 'Duration', 'Number of Repeats', 'Run Type'])
        other_choices = []
        for vals in range(0,4):
            if vals != choice:
                other_choices.append(vals)
        print(res_path, other_choices)
        with open(res_path, 'a') as csvfile:
            duration = round((self.end_time - self.start_time), 3)
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='\"', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow([img_name, choice, alternative, duration, self.repeat_counter, self.run_type])

    def read_desc(self, params):
        with open(params.desc_path, 'r') as f:
            reader = csv.reader(f)
            temp = list(reader)
        temp = temp[1:]  # Remove table headers
        for i, img_entry in enumerate(temp):
            file_name = 'i' + img_entry[0] + '.jpg'
            if i % 2 != 1:
                for j, value in enumerate(img_entry):
                    if j == 1:
                        self.descriptions[file_name] = list()
                    if j != 0 and value != '':
                        self.descriptions[file_name].append(value)
        print(self.descriptions)

    def __init__(self, params):
        self.descriptions = {}
        self.window = tkinter.Tk()
        self.window.title("Trial 1")
        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d+0+0" % (w, h))
        self.read_image_names(params)
        self.read_desc(params)
        self.my_images = dict()
        self.my_image_names = []
        self.label_pairs = set()
        for image in self.image_files:
            full_path = params.img_path + '/' + image
            self.my_images[image] = ImageTk.PhotoImage(Image.open(full_path).resize((750, 500), Image.ANTIALIAS))
            self.get_labels(image)
        self.add_control_cases()
        self.run_trial(params)

#Set parameters:
params = SetParameters()

# ReadInstructions()
#Run experiment:
print(params.img_path, params.desc_path, params.res_path, params.num_img, params.break_size)

RunExperiment(params)
