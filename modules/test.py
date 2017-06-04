from filters import *
import warnings

samplingFreq = 250
Nyquist = samplingFreq / 2

# WARNINGS
warnings.filterwarnings('ignore')

# Signal
rawSignal = readSignal('signal.txt')
rawSignal = normalizeList(rawSignal)
filterOrder = len(rawSignal)

# Filter
# filteredSignal = filterAlphaRhythm(rawSignal, Nyquist)
filteredSignal = bpsFilterSignal(rawSignal, 5, 14, Nyquist)
# filteredSignal = normalizeList(filteredSignal)
# subplot(211)
# plot(genXsignal(len(filteredSignal), samplingFreq), filteredSignal)
# title("Filtered")

# Not filtered spectrum
spectrumRaw = fft.fft(rawSignal)
spectrum = getAmplitudeSpectrum(spectrumRaw)
spectrum = spectrum[0:int((filterOrder / 2))]
subplot(211)
ylim(0, 300)
spectrumCropped = spectrum[0:round(len(spectrum) / 6)]
nyquistCropped = round(Nyquist / 6)
print(str(len(spectrumCropped)))
plot(genXspectrum(len(spectrumCropped), nyquistCropped), spectrumCropped)
# plot(genXspectrum(len(spectrum), Nyquist), spectrum)
title("Not filtered")

# Debug
# print("Length of filtered = " + str(len(filteredSignal)))
# print("Length of raw = " + str(len(rawSignal)))

# Filtered spectrum
spectrumRawFiltered = fft.fft(filteredSignal)
spectrumFiltered = getAmplitudeSpectrum(spectrumRawFiltered)
spectrumFiltered = spectrumFiltered[0:int((filterOrder / 2))]

spectrumFilteredCropped = spectrumFiltered[0:round(len(spectrumFiltered) / 6)]
nyquistFilteredCropped = round(Nyquist / 6)

subplot(212)
plot(genXspectrum(len(spectrumFilteredCropped), nyquistCropped), spectrumFilteredCropped)
# plot(genXspectrum(len(spectrumFiltered), Nyquist), spectrumFiltered)
title("Filtered")

# Spectrum characteristics
maxAmp = maxAmplitude(spectrumFiltered).real
maxAmpFreq = maxAmplitudeFreq(spectrumFiltered, Nyquist)
avAmp = averageAmplitudeInRange(spectrumFiltered, Rhythms.alphaFrom, Rhythms.alphaTo, Nyquist)
print("Max amplitude: " + str(maxAmp) + "\nFrequency: " + str(maxAmpFreq))
print("Average amplitude: " + str(avAmp))
print("Weighted average: " + str(weightedAverageAmplitude(spectrumFiltered, Rhythms.alphaFrom, Rhythms.alphaTo, Nyquist)))

show()