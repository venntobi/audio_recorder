# link to pyaudio wheel
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# pip install C:\Users\user\Downloads\PyAudio-0.2.11-cp38-cp38-win_amd64.whl 

import pyaudio
import wave
import csv 
import os

class Recorder():
    
    def __init__(self, channels=1, rate=48000, chunk=1024):
        
        # check if folder audio_files exists
        # if so, then get the last/biggest file_number
        # else create the folder and set file_number to zero
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

        self.format = pyaudio.paInt16
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.is_recording = False
        self.file_number = file_number

        
    @property
    def is_recording(self):
        return self._recording    
    
    @is_recording.setter
    def is_recording(self, value):
        self._recording = value

    def record(self, filename: str, transcript: str, file_number: int):
        audio = pyaudio.PyAudio()
        wavfile = wave.open(filename + ".wav", 'wb')
        wavfile.setnchannels(self.channels)
        wavfile.setsampwidth(audio.get_sample_size(self.format))
        wavfile.setframerate(self.rate)
        wavstream = audio.open(format=self.format,
                               channels=self.channels,
                               rate=self.rate,
                               input=True,
                               frames_per_buffer=self.chunk)
        
        while self.is_recording: 
            wavfile.writeframes(wavstream.read(self.chunk))
            print("Recording...")
            
        wavstream.stop_stream()
        wavstream.close()
        audio.terminate()
        
        fieldnames = ["wav_filename", "wav_filesize", "transcript"]
        wav_filename = filename.split("/")[1]
        wav_filesize = os.path.getsize(filename + ".wav")
        
        fieldnames = ["wav_filename", "wav_filesize", "transcript"]
        
        if self.file_number % 10 in [7, 8]:
            with open(r'audio_files/dev.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({"wav_filename":wav_filename, "wav_filesize": wav_filesize, "transcript": transcript})
                
        if self.file_number % 10 == 9:
            with open(r'audio_files/test.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({"wav_filename":wav_filename, "wav_filesize": wav_filesize, "transcript": transcript})
            
        else:
            with open(r'audio_files/train.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({"wav_filename":wav_filename, "wav_filesize": wav_filesize, "transcript": transcript})
        

        