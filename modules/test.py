from filters import *
import warnings

samplingFreq = 250
Nyquist = samplingFreq / 2

# WARNINGS
warnings.filterwarnings('ignore')

# Signal
rawSignal = readSignal('signal.txt')
filterOrder = len(rawSignal)
filteredSignal = filterAlphaRhythm(rawSignal, Nyquist)
filteredSignal = normalizeList(filteredSignal)
subplot(211)
plot(genXsignal(len(filteredSignal), samplingFreq), filteredSignal)
title("Filtered")

# Debug
# print("Length of filtered = " + str(len(filteredSignal)))
# print("Length of raw = " + str(len(rawSignal)))

# Spectrum
spectrumRaw = fft.fft(filteredSignal)
spectrum = getAmplitudeSpectrum(spectrumRaw)
spectrum = spectrum[0:int((filterOrder / 2))]

# Spectrum characteristics
maxAmp = maxAmplitude(spectrum).real
maxAmpFreq = maxAmplitudeFreq(spectrum, Nyquist)
avAmp = averageAmplitudeInRange(spectrum, Rhythms.alphaFrom, Rhythms.alphaTo, Nyquist)
print("Max amplitude: " + str(maxAmp) + "\nFrequency: " + str(maxAmpFreq))
print("Average amplitude: " + str(avAmp))
print("Weighted average: " + str(weightedAverageAmplitude(spectrum, Rhythms.alphaFrom, Rhythms.alphaTo, Nyquist)))

# spectrum = normalizeList(spectrumRaw)
subplot(212)
plot(genXspectrum(len(spectrum), Nyquist), spectrum)
title("Spectrum")
show()