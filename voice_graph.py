import numpy as np
# import sounddevice as sd
import soundfile as sf
from scipy import signal
import matplotlib.pyplot as plt
"""
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
"""
"""
def sync_record(filename, duration, fs, channels):
    print('recording')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    sf.write(filename, myrecording, fs)
    print('done recording')
"""
def preprocess(s,fs):
    v = signal.resample(s,10000*len(s)/fs) #decimation
    # VAD (Spectral Power)
    npoint = 1024
    N = len(v)
    # Windowing (hamming)
    win = signal.windows.hamming(1024,False)
    S = signal.fft.stft(v,window=win,noverlap=512)
    # plot spectrogram
    plt.figure()
    plt.title("Spectrogram for Spoken Phrase")
    plt.specgram(v,NFFT=npoint,Fs=10000,noverlap=900)
    plt.xlabel("Samples")
    plt.ylabel("Frequency")
    plt.show()
    I = S * np.conj(S)/N 
    I[0] = I[1] # I gives power spectral density estimate over frequency
    # NR (weiner filter)
    IW = signal.weiner(I)
    xval = np.linspace(0,1,num=len(IW))
    # plot psd est
    plt.figure()
    plt.title("Wiener Filter PSD Estimate")
    plt.plot(xval, IW)
    plt.xlabel("Frequency (w/pi)")
    plt.ylabel("PSD Estimate")
    plt.show()
    # Framing (20-40ms block frames)
    blocklen = 0.03*fs # number of samples in 30ms block
    IW_block = np.reshape(IW,(blocklen,-1))
    # Normalization (Cepstral Mean Normalization CMN)
    ## calculate cepstrum/subtract average from each coeff/(divide by variance)
    C = signal.istft(10*np.log10(IW_block), fs=fs)
    C_CMN = C - np.mean(C,axis=1) # returns time-varying cepstral normalized power estimate
    c_CMN = np.reshape(IW,(1,-1))
    return c_CMN

def main():
    fs = 10000
    duration = 5
    channels = 1
    input("State your name. Press any key when ready.")
    filename = 'C:/Users/NO31574/Downloads/english.mp3'
    #needs some sort of appendage system
    # sync_record(filename, duration, fs, channels)
    print("Done recording.")
    # should use smart terms for these
    s, s_fs = sf.read(filename) # load and sample rough audio file
    c_CMN = preprocess(s,s_fs)


# mp3 issues
if __name__ == "__main__":
    main()