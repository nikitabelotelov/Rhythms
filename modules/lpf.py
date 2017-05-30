from pylab import *
import numpy.fft as fft
import scipy.signal as signal

filterOrder = 1024
samplingFreq = 250
Nyquist = samplingFreq / 2


def genXspectrum(size, NF):
	t = []
	step = float(NF) / float(size)
	for i in range(size):
		t.append(i * step)
	return t

def genXsignal(size, samplingFreq):
	# print("Generated x")
	t = []
	step = float(size) / float(samplingFreq) / float(size)
	for i in range(size):
		t.append(i * step)
	return t

def readSignal(filePath):
	signal = open(filePath, 'r')
	wss = []
	for line in signal:
		ws = float(line)
		wss.append(ws)
	return wss

def mfreqz(b,a=1):
	w,h = signal.freqz(b,a)
	h_dB = 20 * log10 (abs(h))
	subplot(212)
	plot(w/max(w),h_dB)
	ylabel('Magnitude (db)')
	xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
	ylim(-75, 5)
	title(r'Frequency response')

def filterAlphaRhythm(rawSignal, NF):
	return bpsFilterSignal(rawSignal, 8, 13, NF)

def filterBeta1Rhythm(rawSignal, NF):	
	return bpsFilterSignal(rawSignal, 14, 19, NF)

def filterBeta2Rhythm(rawSignal, NF):	
	return bpsFilterSignal(rawSignal, 20, 30, NF)

def filterGammaRhythm(rawSignal, NF):	
	return bpsFilterSignal(rawSignal, 40, 60, NF)

def bpsFilterSignal(rawSignal, fromBound, toBound, NF):
	filterOrder = len(rawSignal)
	lps = signal.firwin(filterOrder, cutoff=fromBound, nyq=NF, window="hamming")
	hps = signal.firwin(filterOrder, cutoff=toBound, nyq=NF, window="hamming")
	ir = -(lps - hps)
	return signal.convolve(ir, rawSignal, mode='same')

def normalizeList(arr):
	return [a / max(arr) for a in arr]

# Signal
rawSignal = readSignal('signal.txt')
filteredSignal = filterAlphaRhythm(rawSignal, Nyquist)
filteredSignal = normalizeList(filteredSignal)
subplot(211)
plot(genXsignal(len(filteredSignal), samplingFreq), filteredSignal)
title("Filtered")

# Debug
print("Length of filtered = " + str(len(filteredSignal)))
print("Length of raw = " + str(len(rawSignal)))

# Spectrum
spectrumRaw = fft.fft(filteredSignal)
spectrum = spectrumRaw[0:(filterOrder / 2)]
spectrum = normalizeList(spectrum)
subplot(212)
plot(genXspectrum(len(spectrum), Nyquist), spectrum)
title("Spectrum")
show()