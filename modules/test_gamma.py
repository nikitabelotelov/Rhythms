from filters import *
import warnings

def shiftArray(array, d):
	for i in range(len(array)):
		array[i] = array[i] + d
	return array

samplingFreq = 250
Nyquist = samplingFreq / 2

# WARNINGS
warnings.filterwarnings('ignore')

# Signal
rawSignal = readSignal('signal.txt')
rawSignal = normalizeList(rawSignal)
filterOrder = len(rawSignal)

# Filter
filteredSignal = filterGammaRhythm(rawSignal, Nyquist)

# Not filtered spectrum
spectrumRaw = fft.fft(rawSignal)
spectrum = getAmplitudeSpectrum(spectrumRaw)
spectrum = spectrum[0:int((filterOrder / 2))]

# Filtered spectrum
spectrumRawFiltered = fft.fft(filteredSignal)
spectrumFiltered = getAmplitudeSpectrum(spectrumRawFiltered)
spectrumFiltered = spectrumFiltered[0:int((filterOrder / 2))]

spectrumFilteredCropped = spectrumFiltered[40:(round(len(spectrumFiltered) / 6)*3)]
nyquistFilteredCropped = round(Nyquist / 6)
nyquistCropped = round(Nyquist / 6)

subplot(212)
xsp = shiftArray(genXspectrum(len(spectrumFilteredCropped), nyquistCropped), 40) 
plot(xsp, spectrumFilteredCropped)

# Spectrum characteristics
maxAmp = maxAmplitude(spectrumFiltered).real
maxAmpFreq = maxAmplitudeFreq(spectrumFiltered, Nyquist)
avAmp = averageAmplitudeInRange(spectrumFiltered, Rhythms.gammaFrom, Rhythms.gammaTo, Nyquist)
print("Max amplitude: " + str(maxAmp) + "\nFrequency: " + str(maxAmpFreq))
print("Average amplitude: " + str(avAmp))
# print(str(len(range(Rhythms.gammaFrom, Rhythms.gammaTo))))
# print(str(len(getSubSpectrum(spectrum, Rhythms.gammaFrom, Rhythms.gammaTo, Nyquist))))
print("Weighted average: " + str(np.average(range(Rhythms.gammaFrom, Rhythms.gammaTo), weights=getSubSpectrum(spectrum, Rhythms.gammaFrom, Rhythms.gammaTo, Nyquist))))

show()