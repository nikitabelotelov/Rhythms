from pylab import *
import numpy.fft as fft
import scipy.signal as signal
import functools

class Rhythms:
	alphaFrom = 9
	alphaTo = 13
	beta1From = 14
	beta1To = 19
	beta2From = 20
	beta2To = 30
	gammaFrom = 40
	gammaTo = 60

def maxAmplitude(spectrum):
	return max(abs(min(spectrum)), max(spectrum))

def maxAmplitudeFreq(spectrum, NF):
	index = spectrum.index(maxAmplitude(spectrum)) 
	return index / len(spectrum) * NF

def averageAmplitudeInRange(spectrum, fromBound, toBound, NF):
	subSpectrum = getSubSpectrum(spectrum, fromBound, toBound, NF)
	return averageAmplitude(subSpectrum)

def averageAmplitude(spectrum):
	return float(sum(spectrum)) / len(spectrum)

def getSubSpectrum(spectrum, fromBound, toBound, NF):
	# print(str(len(spectrum)))
	fromIndex = round((fromBound / NF) * len(spectrum))
	toIndex = round((toBound / NF) * len(spectrum))
	# print('from' + str(fromIndex))
	# print('to' + str(toIndex))
	return spectrum[fromIndex:toIndex]

def weightedAverageAmplitude(spectrum, fromBound, toBound, NF):
	subSpectrum = getSubSpectrum(spectrum, fromBound, toBound, NF)
	avAmp = averageAmplitude(subSpectrum)
	# print('avamp' + str(avAmp))
	# print('avinrange' + str(averageAmplitudeInRange(spectrum, fromBound, toBound, NF)))
	m = len(subSpectrum)
	specSum = 0
	for i in range(len(subSpectrum)):
		specSum += (i + 1) * subSpectrum[i]
	return fromBound - len(subSpectrum) * (specSum / (avAmp * m))

def genXspectrum(size, NF):
	w = []
	step = float(NF) / float(size)
	for i in range(size): 
		w.append(i * step)
	return w

def genXsignal(size, samplingFreq):
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
	# print(str(wss))
	return wss

def mfreqz(b,a=1):
	w,h = signal.freqz(b,a)
	h_dB = 20 * log10 (abs(h))
	subplot(212)
	plot(w/max(w),h_dB)
	ylabel('Magnitude (db)')
	xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
	ylim(-100, 5)
	title('Frequency response')

def filterAlphaRhythm(rawSignal, NF):
	return bpsFilterSignal(rawSignal, Rhythms.alphaFrom, Rhythms.alphaTo, NF)

def filterBeta1Rhythm(rawSignal, NF):	
	return bpsFilterSignal(rawSignal, Rhythms.beta1From, Rhythms.beta1To, NF)

def filterBeta2Rhythm(rawSignal, NF):	
	return bpsFilterSignal(rawSignal, Rhythms.beta2From, Rhythms.beta2To, NF)

def filterGammaRhythm(rawSignal, NF):	
	return bpsFilterSignal(rawSignal, Rhythms.gammaFrom, Rhythms.gammaTo, NF)

def bpsFilterSignal(rawSignal, fromBound, toBound, NF):
	ir = bpsIR(rawSignal, fromBound, toBound, NF)
	return signal.convolve(ir, rawSignal, mode='same')

def bpsIR(rawSignal, fromBound, toBound, NF):
	filterOrder = len(rawSignal)
	lps = signal.firwin(filterOrder, cutoff=fromBound, nyq=NF, window="hamming")
	hps = signal.firwin(filterOrder, cutoff=toBound, nyq=NF, window="hamming")
	return -(lps - hps)

def normalizeList(arr):
	av = averageAmplitude(arr)
	l = [a - av for a in arr]
	# print(str(l))
	return l

def getAmplitudeSpectrum(spectrum):
	return [abs(a) for a in spectrum]