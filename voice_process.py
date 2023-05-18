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

def preprocess(s,fs):
    v = signal.resample(s,10000*len(v)/fs) #decimation
    # VAD (Spectral Power)
    npoint = 1024
    N = len(v)
    # Windowing (hamming)
    win = signal.windows.hamming(1024,False)
    S = signal.fft.stft(v,window=win,noverlap=512)
    I = S * np.conj(S)/N 
    I[0] = I[1] # I gives power spectral density estimate over frequency
    # NR (weiner filter)
    IW = signal.weiner(I)
    # Framing (20-40ms block frames)
    blocklen = 0.03*fs # number of samples in 30ms block
    IW_block = np.reshape(IW,(blocklen,-1))
    # Normalization (Cepstral Mean Normalization CMN)
    ## calculate cepstrum/subtract average from each coeff/(divide by variance)
    C = signal.istft(np.10*np.log10(IW_block), fs=fs)
    C_CMN = C - np.mean(C,axis=1) # returns time-varying cepstral normalized power estimate
    c_CMN = np.reshape(IW,(1,-1))
    return c_CMN

def levdur(r,p)
    a = np.zeros(p+1)
    k = np.zeros(p)
    Jo = np.zeros(p+1)
    J=r[0]
    Jo[0]=J
    ebta=r[1]
    k[0] = -beta/J
    a[0]=k[0]
    J=J+beta*k[0]
    Jo[1]=J
    for m in range(1,p-1)
        beta[r[1:m]].T @ np.flipud(a[0:m-1])+r[m]
        k[m]=-beta/J 
        a[0:m]=[(a[0:m-1]).T, 0].T + [np.flipud(a[0:m-1]).T, 1].T @ k[m]
    a[1:p+1] = a[0:p]
    a[0] = 1
    return a

def signal_fex(S,fs,enroll):
    # Feature Selection (from pymir)
    numFilters = 32
    x = S
    n = len(x)
	m = 2 ** (1.0 / 6)
	f2 = 110.0
	f1 = f2 / m
	f3 = f2 * m
	fb = scipy.array(scipy.zeros(numFilters))
	for i in range(numFilters):
		fb[i] = np.absolute(fbwin(x, fs, f1, f2, f3))
		f1 = f2
		f2 = f3
 		f3 = f3 * m
	coeff = scipy.fftpack.dct(scipy.log(fb), type = 2, norm = 'ortho') # Alternative (and vectorized) MFCC computation from Steve Tjoa
    # LAR
    a = levdur(S,11)
    A = np.zeros(np.shape(a))
    for k in range(0,len(a))
        A[k] = np.log((1-a[k])/(1+a[k]))
    f_vec = [coeff[0:10], A[0:10]]
    # Estimate mean and covariance
    f_mean = np.mean(f_vec) # scalar
    f_cov = np.cov(f_vec) # matrix
    # Enroll option
    if enroll == True:
        np.save('/data/means.npy', f_mean)
        np.save('/data/covs.npy', f_cov)
    return f_vec

def match_score(x,mu,C):
    # x is an observed feature vector
    score = (2*np.pi)**(-k/2)@np.absolute(C)**(-1/2) * np.exp(-0.5*(x-mu).T @ C**(-1) @ (x-mu))
    return score

def verify_sig(f_vec):
    # Hypothesis test (Bhattacharyya Distance?)
    means_data = np.load('/data/means.npy')
    covs_data = np.load('/data/covs.npy')
    mean_r = np.mean(means_data)
    mean_cov = np.mean(mean_cov,3)
    score_data = match_score(f_vec,mean_r,mean_cov)
    score_model = match_score(mean_r,mean_r,mean_cov)
    lambda_a = score_data/score_model
    # divergence shape and bc distance? or just "which gaussian"
    T = 0
    if lambda_a < T:
        return True
    else:
        return False

def main():
    fs = 10000
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
        enroll=True
        enroll_num += 1
        input("State your name. Press any key when ready.")
        filename = dir_name + "common_voice_en_" + enroll_num  + ".wav" #needs some sort of appendage system
        sync_record(filename, duration, fs, channels)
        print("Done recording.")
    else:
        enroll=False
        input("State your name. Press any key when ready.")
        filename = dir_name + "verify" + ".wav"
        sync_record(filename, duration, fs, channels)
        print("Done recording.")
    # should use smart terms for these
    s, s_fs = sf.read(filename) # load and sample rough audio file
    c_CMN = preprocess(s,s_fs)
    f_vec = signal_fex(c_CMN,fs,enroll)
    decision = verify_sig(f_vec)
    # now what was it you wanted to do?


# mp3 issues
if __name__ == "__main__":
    main()