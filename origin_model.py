import numpy as np
import matplotlib.pyplot as plt

# constants
h = 6.62607015e-34  # Planck constant (J·s)
c = 2.99792458e8    # Speed of light (m/s)
k = 1.380649e-23    # Boltzmann constant (J/K)

def planck(wavelength, T):
    """Blackbody spectral radiance via Planck's Law."""
    a = 2.0 * h * c**2 / (wavelength**5)
    b = np.exp(h * c / (wavelength * k * T)) - 1.0
    return a / b

def plot_blackbody_2d(temperatures, wavelength_range):
    """Static 2D blackbody spectra using Matplotlib."""
    wavelengths = np.linspace(wavelength_range[0], wavelength_range[1], 500)
    fig, ax = plt.subplots(figsize=(10, 6))
    for T in temperatures:
        radiance = planck(wavelengths, T)
        ax.plot(wavelengths * 1e9, radiance, label=f"{T} K")

    ax.set_title("Blackbody Radiation Spectra")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Spectral Radiance (W·sr⁻¹·m⁻³)")
    ax.legend()
    ax.grid(True)
    return fig

# 🔸 NEW: Interactive 3D version using Plotly
import plotly.graph_objects as go

def plot_blackbody_3d_interactive(temperatures, wavelength_range):
    """Interactive 3D blackbody radiation surface plot using Plotly."""
    wavelengths = np.linspace(wavelength_range[0], wavelength_range[1], 300)
    W, T = np.meshgrid(wavelengths, temperatures)
    Z = planck(W, T)

    fig = go.Figure(data=[go.Surface(
        x=W * 1e9,
        y=T,
        z=Z,
        colorscale="Plasma"
    )])

    fig.update_layout(
        scene=dict(
            xaxis_title="Wavelength (nm)",
            yaxis_title="Temperature (K)",
            zaxis_title="Spectral Radiance (W·sr⁻¹·m⁻³)"
        ),
        width=750,
        height=500,
        margin=dict(l=0, r=0, b=0, t=50)
    )
    return fig