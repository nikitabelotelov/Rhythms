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
filteredSignal = filterBeta2Rhythm(rawSignal, Nyquist)

# Not filtered spectrum
spectrumRaw = fft.fft(rawSignal)
spectrum = getAmplitudeSpectrum(spectrumRaw)
spectrum = spectrum[0:int((filterOrder / 2))]

# Filtered spectrum
spectrumRawFiltered = fft.fft(filteredSignal)
spectrumFiltered = getAmplitudeSpectrum(spectrumRawFiltered)
spectrumFiltered = spectrumFiltered[0:int((filterOrder / 2))]

spectrumFilteredCropped = spectrumFiltered[20:(round(len(spectrumFiltered) / 6)*2)]
nyquistFilteredCropped = round(Nyquist / 6)
nyquistCropped = round(Nyquist / 6)

subplot(212)
xsp = shiftArray(genXspectrum(len(spectrumFilteredCropped), nyquistCropped), 20) 
plot(xsp, spectrumFilteredCropped)

# Spectrum characteristics
maxAmp = maxAmplitude(spectrumFiltered).real
maxAmpFreq = maxAmplitudeFreq(spectrumFiltered, Nyquist)
avAmp = averageAmplitudeInRange(spectrumFiltered, Rhythms.beta2From, Rhythms.beta2To, Nyquist)
print("Max amplitude: " + str(maxAmp) + "\nFrequency: " + str(maxAmpFreq))
print("Average amplitude: " + str(avAmp))
print("Weighted average: " + str(np.average(range(Rhythms.beta2From, Rhythms.beta2To), weights=getSubSpectrum(spectrum, Rhythms.beta2From, Rhythms.beta2To, Nyquist)[0:10])))

show()