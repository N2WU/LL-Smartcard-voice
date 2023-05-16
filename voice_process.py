"""
This program serves as an experimental testbed for the Common Access Card (CAC) encryption and decryption
Most of the theory is taken from Campbell's "Speaker Recognition: A tutorial"
"""
import numpy as np
import cryptography
import sounddevice as sd
import soundfile as sf
from scipy import signal
import time 
import re
import os

def mic_check():
    mics=sd.query_devices()
    default_devices=sd.default.device
    default_input=default_devices[0]
    default_output=default_devices[1]
    # prints all available devices 
    for i in range(len(mics)):
        print(mics[i])
    # can set default device easily with 
    # sd.default.device = 0
def sync_record(filename, duration, fs, channels):
    print('recording')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    sf.write(filename, myrecording, fs)
    print('done recording')
    # 

def signal_ack(s,duration):
    # Decimate to fs
    v = signal.resample(s,duration*3000)


def signal_extr(v):
    # Linear prediction
    win = signal.windows.hamming(1024,False)
    S = signal.fft.stft(v,window=win,noverlap=512)
    # MFCC
    
    # LAR

    # LSP

    # LP Cepstrum

    # V

def signal_pm():
    # Feature Selection

    # Estimate mean and covariance

    # Enroll option

def enroll_user():
    # Store training and reference data w/ means + covariances
    
def verify_sig():
    # Hypothesis test (Bhattacharyya Distance?)

# mp3 issues
if __name__ == "__main__":
    fs = 16000
    duration = 5
    channels = 1
    choice = input("Enroll [E] or verify [V]?")
    dir_name = 'D:/pearc/Documents/projects/speech/datasets/en/clips/'
    # Get list of all files in a given directory sorted by name
    list_of_files = sorted( filter( lambda x: os.path.isfile(os.path.join(dir_name, x)),
                        os.listdir(dir_name) ) )
    enroll_last = max(list_of_files).split("en_",2)
    enroll_num = enroll_last[1]
    if choice == "E":
        enroll_num += 1
        input("State your name. Press any key when ready.")
        filename = dir_name + "common_voice_en_" + enroll_num  + ".wav" #needs some sort of appendage system
        sync_record(filename, duration, fs, channels)
        print("Done recording.")
    else:
        input("State your name. Press any key when ready.")
        filename = dir_name + "verify" + ".wav"
        sync_record(filename, duration, fs, channels)
        print("Done recording.")
    # should use smart terms for these
    s, s_fs = sf.read(filename) # load and sample rough audio file
    v = signal_ack(s,duration)
