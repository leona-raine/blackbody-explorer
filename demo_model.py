import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

h = 6.62607015e-34  # planck constant
c = 2.99792458e8    # speed of light
k = 1.380649e-23    # boltzmann constant


def planck_law(wavelength, T):
    wavelength = np.asarray(wavelength, dtype=float)
    small = 1e-30
    wavelength = np.maximum(wavelength, small)

    exponent = (h * c) / (wavelength * k * T)
    with np.errstate(over='ignore', invalid='ignore'):
        denom = np.exp(exponent) - 1.0
        radiance = (2.0 * h * c**2) / (wavelength**5 * denom)
    return radiance


def plot_blackbody_2d(temperatures, wl_min_m, wl_max_m, n_points=500): # still static atm
    wavelengths = np.linspace(wl_min_m, wl_max_m, n_points)
    fig, ax = plt.subplots(figsize=(10, 6))
    for T in temperatures:
        radiance = planck_law(wavelengths, T)
        ax.plot(wavelengths * 1e9, radiance, label=f"{T} K")
    ax.set_title("Blackbody Radiation Spectra")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Spectral Radiance (W·sr⁻¹·m⁻³)")
    ax.grid(True)
    ax.legend()
    return fig

def plot_blackbody_3d_interactive(temperatures, wavelength_range): # 3d is now interactive
    wavelengths = np.linspace(wavelength_range[0], wavelength_range[1], 300)
    W, T = np.meshgrid(wavelengths, temperatures)
    Z = planck_law(W, T)

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

def plot_blackbody_3d_animated(
    wl_min_nm=380,
    wl_max_nm=750,
    temp_min=3000,
    temp_max=10000,
    n_wavelengths=200,
    n_frames=60,
    duration=80,
    loop=True,
):

    wl_min_m = wl_min_nm * 1e-9
    wl_max_m = wl_max_nm * 1e-9

    wavelengths = np.linspace(wl_min_m, wl_max_m, n_wavelengths) 
    wavelengths_nm = wavelengths * 1e9

    frame_temps = np.linspace(temp_min, temp_max, n_frames)

    frames = []
    for T in frame_temps:
        z = planck_law(wavelengths, T)
        trace = go.Scatter3d(
            x=wavelengths_nm,
            y=np.full_like(wavelengths_nm, T),
            z=z,
            mode="lines",
            line=dict(color="orange", width=4),
            hoverinfo="x+y+z",
            name=f"{T:.0f} K"
        )
        frames.append(go.Frame(data=[trace], name=f"{T:.0f}"))

    initial_z = planck_law(wavelengths, frame_temps[0])
    base_trace = go.Scatter3d(
        x=wavelengths_nm,
        y=np.full_like(wavelengths_nm, frame_temps[0]),
        z=initial_z,
        mode="lines",
        line=dict(color="orange", width=4),
        hoverinfo="x+y+z",
    )

    play_args = [None, {
        "frame": {"duration": duration, "redraw": True},
        "fromcurrent": True,
        "transition": {"duration": int(duration / 2)}
    }]

    if loop:
        reversed_frames = frames[::-1]
        frames_for_layout = frames + reversed_frames[1:-1]
    else:
        frames_for_layout = frames

    fig = go.Figure(
        data=[base_trace],
        layout=go.Layout(
            scene=dict(
                xaxis=dict(title="Wavelength (nm)"),
                yaxis=dict(title="Temperature (K)"),
                zaxis=dict(title="Spectral Radiance"),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
            ),
            margin=dict(l=0, r=0, b=0, t=60),
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    y=0.05,
                    x=0.05,
                    xanchor="left",
                    yanchor="bottom",
                    buttons=[
                        dict(label="▶ Play", method="animate", args=play_args),
                        dict(label="⏸ Pause", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}])
                    ],
                )
            ],
        ),
        frames=frames_for_layout
    )

    slider_steps = []
    total_frames = len(frames_for_layout)
    for i, fr in enumerate(frames_for_layout):
        step = dict(
            method="animate",
            args=[
                [fr.name],
                {"mode": "immediate", "frame": {"duration": 0, "redraw": True}, "transition": {"duration": 0}}
            ],
            label=str(i + 1)
        )
        slider_steps.append(step)

    fig.update_layout(
        sliders=[dict(
            active=0,
            steps=slider_steps,
            x=0.12, y=0, len=0.8
        )]
    )

    return fig