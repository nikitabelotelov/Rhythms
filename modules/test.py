from filters import *

filterOrder = 1024
samplingFreq = 250
Nyquist = samplingFreq / 2

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
# spectrum = normalizeList(spectrumRaw)
subplot(212)
plot(genXspectrum(len(spectrum), Nyquist), spectrum)
title("Spectrum")
show()