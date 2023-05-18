% This code acts as a processing platform and sandbox for campbell speech
% recognition tutorial
fs = 10e3;

%% Import signal

[s, Fs_test] = audioread("D:\pearc\Documents\projects\speech\datasets\en\clips\common_voice_en_36530278.mp3");

%% Acquire Signal

v = resample(s,Fs_test,fs); %decimated basically?

%% Extract Signal Components
%mfcc
win = hann(1024,"periodic");
S = stft(v,"Window",win,"OverlapLength",512,"Centered",false);
coeffs = mfcc(S,fs);
nbins = 60;
coefficientToAnalyze = 4;
histogram(coeffs(:,coefficientToAnalyze+1),nbins,"Normalization","pdf")
title(sprintf("Coefficient %d",coefficientToAnalyze))

spectralCentroid(v,fs);
%lar

%lsp

%v



%% Pattern matching

%% Hypothesis testing