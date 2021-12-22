import tkinter as tk
import pandas as pd 
from threading import Thread
from recorder import Recorder
import os 
import csv 
from time import sleep

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Deepspeech Recording Tool")
        self.geometry('550x350')
        
        self.is_recording_label = tk.Label(self, text="Waiting")

        self.start_recording_button = tk.Button(self, text="Start", command=lambda: Thread(target=self.start_rec).start(), width=15)
        self.stop_recording_button = tk.Button(self, text="Stop", command=self.stop_rec, width=15)

        self.start_recording_button.grid(row=0, column=0,padx=5, pady=5)
        self.stop_recording_button.grid(row=0, column=1,padx=5, pady=5)
        self.is_recording_label.grid(row=1, column=0,padx=5, pady=5)
        
        self.sentences = pd.read_csv("sentences.csv")
        self.current_sentence = self.sentences.sample(1).iloc[0]["Satz"]
        self.rec = Recorder()
        
        self.sentence_label = tk.Label(self, text=self.current_sentence, wraplengt=200, bg="white", font=(None, 15))
        self.sentence_label.grid(row=0, column=2,padx=5, pady=5)
        
        self.number = self.file_number()
        


    def select_sentence(self):
        return self.sentences.sample(1).iloc[0]["Satz"]

    def file_number(self):
        if os.path.exists("audio_files"):
            list_of_files = os.listdir("audio_files")
            if len(list_of_files) == 0:
                file_number = 0
            else:
                paths = [os.path.join("audio_files/", basename) for basename in list_of_files]
                latest_file = max(paths, key=os.path.getctime)
                file_number = int(latest_file.split("/")[1].split(".")[0].split("_")[1]) + 1
        else:
            os.mkdir("audio_files")
            file_number = 0
            
        return file_number

    # def save_transcript(self, transcript, filename):
    #     fieldnames = ["wav_filename", "wav_filesize", "transcript"]
    #     wav_filesize = os.path.getsize(filename)
    #     with open(r"audio_files/clips.csv", 'a', newline='') as csvfile:
    #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #         writer.writerow({"wav_filename": fieldnames, "wav_filesize": wav_filesize, "transcript": transcript})
            
    def start_rec(self):
        if self.rec.is_recording:
            print("Already recording!")
        else:
            number = self.number
            self.number += 1
            filename = "audio_files/file_" + str(number)
            self.is_recording_label["text"] = "Live"
            self.is_recording_label["bg"] = "red"
            self.rec.is_recording = True
            self.rec.record(filename, self.current_sentence, number)
        
    def stop_rec(self):
        if not self.rec.is_recording:
            print("Es läuft gerade keine Aufnahme!")
        else:
            self.rec.is_recording = False
            self.is_recording_label["text"] = "Waiting"
            self.is_recording_label["bg"] = "gray"
            self.current_sentence = self.select_sentence()
            self.sentence_label["text"] = self.current_sentence


if __name__ == "__main__":
    root = Root()
    root.mainloop()