import tkinter
import tkinter as ttk
import csv
import time
from functools import partial
from PIL import ImageTk, Image
from os import path
import os
import datetime

# Experiment Global Variables - Should be consistent between runs
left_key = "1"
right_key = "2"
repeat_key = "<Key-space>"
continue_key = "<Key-space>"
pause_experiment_key = "<Return>"
result_directory = "./results/"
label_pairs_directory = "../New_Assets/LabelPairs/test.tsv"
max_repeat = 7
participant_name = ""
break_trial=200


def beep(beep_type=None):
    if beep_type == "left":
        duration = 0.2  # second
        freq = 640  # Hz
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
    elif beep_type == "right":
        duration = 0.2  # second
        freq = 540  # Hz
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
    else:
        duration = 0.2  # second
        freq = 240  # Hz
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))


def say(text_to_say=None):
    os.system('say "' + text_to_say + ' "')


class LabelPair:
    image_name = ""
    left_desc = ""
    left_desc_type = ""
    right_desc = ""
    right_desc_type = ""
    trial_type = ""

    def __init__(self, in_image_name, in_left_desc, in_left_desc_type, in_right_desc, in_right_desc_type, in_trial_type):
        self.image_name = in_image_name
        self.left_desc = in_left_desc
        self.left_desc_type = in_left_desc_type
        self.right_desc = in_right_desc
        self.right_desc_type = in_right_desc_type
        self.trial_type = in_trial_type


class SetParameters:
    def get_params(self):
        def save_parameters():
            global participant_name
            self.img_path = img_path_box.get()
            self.desc_path = desc_path_box.get()
            self.nonsense_path = nonsense_path_box.get()
            participant_name = res_path_box.get()
            now = datetime.datetime.now()
            self.res_path = result_directory + participant_name + "-" + str(now.day) + "-" + str(now.month) + "-" + str(now.year) + "-" + \
                str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + ".csv"
            window.destroy()

        window = tkinter.Tk()
        window.title("Set Experiment Parameters")
        frame = ttk.Frame(window)
        frame.grid(column="0", row="0", sticky=('N', 'W', 'E', 'S'))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        field_labels = ["Image Location", "Label Pair Location", "Participant Initials"]

        img_path_box = ttk.StringVar()
        desc_path_box = ttk.StringVar()
        res_path_box = ttk.StringVar()
        nonsense_path_box = ttk.StringVar()

        tkinter.Label(frame, text=field_labels[0]).grid(row=0, column=0, sticky='E')
        img_entry = tkinter.Entry(frame, textvariable=img_path_box)
        img_entry.insert(0, '../New_Assets/Images/BenchmarkIMAGES')
        img_entry.grid(row=0, column=1, sticky='W')

        tkinter.Label(frame, text=field_labels[1]).grid(row=1, column=0, sticky='E')
        desc_entry = tkinter.Entry(frame, textvariable=desc_path_box)
        desc_entry.insert(0, '../New_Assets/LabelPairs/test.tsv')
        desc_entry.grid(row=1, column=1, sticky='W')

        tkinter.Label(frame, text=field_labels[2]).grid(row=2, column=0, sticky='E')
        res_entry = tkinter.Entry(frame, textvariable=res_path_box)
        res_entry.insert(0, 'noname')
        res_entry.grid(row=2, column=1, sticky='W')

        tkinter.Button(window, text="Run Experiment", command=save_parameters).grid(row=5)
        window.mainloop()

    def __init__(self):
        self.img_path = ''
        self.desc_path = ''
        self.res_path = ''
        self.label_pairs_path = ''
        self.get_params()


class ReadInstructions:
    @staticmethod
    def ignore(event):
        print("Keys are locked - ignore key presses")
        return "break"

    def bind_keys(self):
        which_key = self.which_key
        if which_key == 'left':
            self.window.bind(left_key, self.test_left_key)
        elif which_key == 'right':
            self.window.bind(right_key, self.test_right_key)
        elif which_key == 'repeat':
            self.window.bind(repeat_key, self.test_repeat_key)
        elif which_key == 'exit':
            self.window.bind("<space>", self.exit_window)

    def read_instructions(self):
        say('A series of photos will be shown. Each photo will have two captions associated with the photo. ')
        say('Each caption will be denoted with left or right at the beginning. '
            'If you prefer the left caption, press the left key. If you prefer the right caption,'
            'press the right key. To repeat both captions, press the space bar.')
        time.sleep(1)
        say('Before we start, let\'s test the keys. Press the left key now')
        self.which_key = 'left'
        self.window.after(1, self.bind_keys)

    def test_left_key(self, event):
        self.window.bind(left_key, self.ignore)
        say('You have just pressed the left key. When you select the left key, this tone will sound:')
        time.sleep(0.5)
        beep('left')
        time.sleep(0.5)
        say('Now, let\'s test the right key. Press the right key now.')
        self.which_key = 'right'
        self.window.after(1, self.bind_keys)

    def test_right_key(self, event):
        self.window.bind(right_key, self.ignore)
        say('You have just pressed the right key. When you select the right key, this tone will sound:')
        time.sleep(0.5)
        beep('right')
        time.sleep(0.5)
        say('Now, let\'s test the repeat key. Press the repeat key now.')
        self.which_key = 'repeat'
        self.window.after(1, self.bind_keys)

    def test_repeat_key(self, event):
        self.window.bind("<space>", self.ignore)
        say('You have just pressed the repeat key. When this key is pressed, the description will repeat.')
        time.sleep(0.5)
        say('You are now ready to start the experiment. Press the space key to begin')
        self.which_key = 'exit'
        self.window.after(1, self.bind_keys)

    def exit_window(self, event):
        self.window.destroy()

    def __init__(self):
        self.window = tkinter.Tk()
        self.which_key = ''
        self.window.title("Read Instructions")
        label = ttk.Label(self.window, text="SPEAKING INSTRUCTIONS, PRESS SPACE TO CONTINUE")
        label.pack()
        self.window.tkraise()
        self.window.update()
        self.read_instructions()
        self.window.mainloop()


class PauseExperiment:
    @staticmethod
    def read_repeats_pause():
        say('This experiment has been paused. Please contact the proctor for assistance.')

    @staticmethod
    def read_break_pause():
        say('This experiment has been paused for a break. Notify the proctor to resume the experiment')

    def exit_window(self, event):
        say('This trial will now be resumed')
        self.window.destroy()

    def __init__(self, type):
        self.window = tkinter.Tk()
        self.window.title("Pause Experiment")
        if type == 'repeats':
            label = ttk.Label(self.window, text="PAUSING EXPERIMENT -- TOO MANY REPEATS")
            label.pack()
            self.window.tkraise()
            self.window.update()
            self.read_repeats_pause()
        elif type == 'break':
            label = ttk.Label(self.window, text="PAUSING EXPERIMENT -- REGULAR BREAK")
            label.pack()
            self.window.tkraise()
            self.window.update()
            self.read_break_pause()
        self.window.bind(continue_key, self.exit_window)
        self.window.wait_window()


class RunExperiment:
    @staticmethod
    def ignore(event):
        print("Keys are locked - ignore key presses")
        return "break"

    def take_break(self, event):
        start = time.time()
        PauseExperiment('break')
        end = time.time()
        duration = round(end - start, 3)
        with open(self.res_path, 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='\"', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["Took break. Length - " + str(duration)])

    def lock_key(self, event=None):
        self.window.bind(left_key, self.ignore)
        self.window.bind(right_key, self.ignore)
        self.window.bind(repeat_key, self.ignore)
        self.window.bind(pause_experiment_key, self.ignore)

    def unlock_key(self, event=None):
        self.window.bind(left_key, self.top_left_act)
        self.window.bind(right_key, self.top_right_act)
        self.window.bind(repeat_key, self.repeat_label)
        self.window.bind(pause_experiment_key, self.take_break)


    def read_label(self, event=None):
        self.lock_key()
        time.sleep(0.5)
        say('left: ' + self.left_label.replace('\'', '\\\''))
        time.sleep(1)
        time.sleep(0.5)
        say('right: ' + self.right_label.replace('\'', '\\\''))
        self.window.after(1, self.unlock_key)

    def repeat_label(self, event=None):
        self.repeat_label_counter += 1
        self.read_label()

    def run_trial(self, res_path):
        self.window.title("Trial " + str(self.trial_number))
        img_frame = ttk.Frame(self.window)
        img_frame.pack()

        button_frame = ttk.Frame(self.window)
        button_frame.pack()

        curr_label_pair = self.label_pairs.pop(0)
        self.curr_image_name = curr_label_pair.image_name
        self.left_label = curr_label_pair.left_desc
        self.left_label_type = curr_label_pair.left_desc_type
        self.right_label = curr_label_pair.right_desc
        self.right_label_type = curr_label_pair.right_desc_type
        self.run_type = curr_label_pair.trial_type
        self.img_canvas = ttk.Canvas(img_frame, width=self.my_images[self.curr_image_name].width(),
                                     height=self.my_images[self.curr_image_name].height())
        self.img_canvas.pack()
        self.repeat_label_counter = 0
        self.img_on_canvas = self.img_canvas.create_image(0, 0, anchor='nw', image=self.my_images[self.curr_image_name])

        font = "Courier"
        font_size = 30
        self.top_left_act = partial(self.choose_string, 'left', res_path)
        self.top_left_bttn = tkinter.Button(button_frame, text=self.left_label, command=self.top_left_act,
                                            font=(font, font_size))
        self.top_left_bttn.pack()

        self.top_right_act = partial(self.choose_string, 'right', res_path)
        self.top_right_bttn = tkinter.Button(button_frame, text=self.right_label, command=self.top_right_act,
                                             font=(font, font_size))
        self.top_right_bttn.pack()
        self.window.tkraise()
        self.window.update()
        self.read_label()
        self.repeat_key_counter = 0
        self.last_key = None
        self.write_repeat = False
        self.window.after(1, self.unlock_key)
        self.start_time = time.time()
        self.window.mainloop()

    def choose_string(self, pressed, res_path, event=None):
        self.end_time = time.time()
        self.lock_key()
        if self.trial_number == break_trial:
            PauseExperiment('break')
        if self.repeat_key_counter >= max_repeat:
            PauseExperiment('repeats')
            self.repeat_key_counter = 0
            self.write_repeat = True
        self.key_pressed = pressed
        beep(pressed)
        time.sleep(1)
        if self.last_key == pressed:
            self.repeat_key_counter += 1
        else:
            self.repeat_key_counter = 1
            self.last_key = pressed
        say('next image')
        self.write_entry(res_path, self.curr_image_name, self.top_left_bttn['text'], self.top_right_bttn['text'])
        self.write_repeat = False
        if len(self.label_pairs) == 0:
            say('This experiment is now over. Please call over the proctor to end the session.')
            self.window.destroy()
        else:
            self.trial_number += 1
            self.repeat_label_counter = 0
            curr_label_pair = self.label_pairs.pop(0)
            self.curr_image_name = curr_label_pair.image_name
            self.left_label = curr_label_pair.left_desc
            self.left_label_type = curr_label_pair.left_desc_type
            self.right_label = curr_label_pair.right_desc
            self.right_label_type = curr_label_pair.right_desc_type
            self.run_type = curr_label_pair.trial_type
            self.window.title("Trial " + str(self.trial_number))
            self.img_canvas.itemconfig(self.img_on_canvas, image=self.my_images[self.curr_image_name])
            self.img_canvas.config(width=self.my_images[self.curr_image_name].width(),
                                   height=self.my_images[self.curr_image_name].height())
            self.top_left_bttn.configure(text=self.left_label)
            self.top_right_bttn.configure(text=self.right_label)
            self.top_left_bttn.pack()
            self.top_right_bttn.pack()
            self.window.update()
            self.read_label()
            self.window.after(1, self.unlock_key)
            self.start_time = time.time()

    def write_entry(self, res_path, img_name, left, right):
        if path.isfile(res_path) is not True:
            with open(res_path, 'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='\"', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(['Participant Initials', 'Image name', 'Left Option', 'Left Label Type', 'Right Option', 'Right Label Type', 'Duration',
                                     'Number of Command Repeats', 'Run Type', 'Key Chosen',
                                     'Passed Repeat Key Threshold'])
        with open(res_path, 'a') as csvfile:
            duration = round((self.end_time - self.start_time), 3)
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='\"', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow([participant_name, img_name, left, self.left_label_type, right, self.right_label_type, duration,
                                    self.repeat_label_counter, self.run_type, self.key_pressed, self.write_repeat])

    def read_desc(self, desc_path):
        with open(desc_path, 'r') as f:
            reader = csv.reader(f, delimiter='\t') # TSV File
            temp = list(reader)
        temp = temp[1:]  # Remove table headers
        for row in temp:
            self.image_files.add(row[0])
            new_pair = LabelPair(row[0], row[1], row[2], row[3], row[4], row[5])
            self.label_pairs.append(new_pair)

    def __init__(self, in_params):
        self.descriptions = {}
        self.image_files = set()
        self.label_pairs = list()
        self.window = tkinter.Tk()
        self.lock_key()
        self.window.geometry("%dx%d+0+0" % (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.read_desc(in_params.desc_path)
        self.res_path = in_params.res_path
        self.label_pairs_path = in_params.label_pairs_path
        self.my_images = dict()
        self.trial_number = 1
        self.curr_image_name = ''
        self.left_label = ''
        self.left_label_type = ''
        self.right_label = ''
        self.right_label_type = ''
        self.run_type = ''
        self.key_pressed = ''
        self.last_key = ''
        self.start_time = 0
        self.end_time = 0
        self.repeat_key_counter = 0
        self.repeat_label_counter = 0
        self.top_left_act = None
        self.top_left_bttn = None
        self.write_repeat = None
        self.top_right_act = None
        self.top_right_bttn = None
        self.img_canvas = None
        self.img_on_canvas = None
        for image in self.image_files:
            full_path = in_params.img_path + '/' + image
            self.my_images[image] = ImageTk.PhotoImage(Image.open(full_path))
        self.run_trial(in_params.res_path)


params = SetParameters()
# ReadInstructions()
RunExperiment(params)
