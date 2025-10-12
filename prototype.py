"""
Additional note:
Originally on Jupyer notebook as the newer version of vscode cannot launch juypter extension

"""


import numpy as np # for numerical computations and array handling
import matplotlib.pyplot as plt # visualize blackbody spectra arrays

# constants
h = 6.62607015e-34 # in joule-sec
c = 2.99792458e8 # speed of light in m/s
k = 1.380649e-23 # Boltzmann constant in joule/kelvin

def planck(wavelength, T):
    """
    Calculating blackbody spectral radiance using Planck's Law.

    Parameters:
    1) wavelength
    - np.array or float
    - in meters

    2) T
    - float
    - in kelvin

    when return:
    spectral rediance in W·sr^-1·m^-3

    """

    a = 2.0*h**c**2 / (wavelength**5)  # numerator = 2*h*c^2 / λ^5
    b = np.exp(h*c / (wavelength*k*T)) - 1.0 # denominator = exp(h*c / (λ*k*T)) - 1
    return a / b

def plot_spectrum(temperatures, wavelength_range):
    """
    Instruction: Plot blackbody spectra for multiple temperatures.

    Parameters:
    1) T
    - list of float
    - in kelvin

    2) wavelength_range
    - tuple
    - in meters
    
    """

    wavelengths = np.linspace(wavelength_range[0], wavelength_range[1], 500) # create 500 points linear space between start and end wavelength
    plt.figure(figsize=(10,6)) # set plot size 10x6

    for T in temperatures:
        radiance = planck(wavelengths, T) # spectral radiance for each temperature computation
        plt.plot(wavelengths*1e9, radiance, label=f'{T} K') # plot wavelength in nanometers against radiance

    plt.title("Blackbody Radiation Spectra")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Spectral Radiance W·sr⁻¹·m⁻³)")
    plt.legend() # display temp labels
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # sample usage
    temps = [3000, 4500, 6000] # measurements should be in kelvin
    wl_range = (1e-7, 3e-6) # measurements should be in nanometers ranging within 100nm - 3000nm
    plot_spectrum(temps, wl_range)