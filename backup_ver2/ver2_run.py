import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from demo_model import plot_blackbody_3d_interactive, planck_law

st.set_page_config(layout="wide", page_title="Blackbody Explorer")

st.title("Blackbody Explorer – 3D Animated & 2D Static")

col_controls, col_plot = st.columns([1, 3])

with col_controls:
    st.header("Controls")

    wl_min_nm = st.number_input("Start wavelength (nm)", 10, 20000, 380)
    wl_max_nm = st.number_input("End wavelength (nm)", 10, 20000, 750)
    if wl_max_nm <= wl_min_nm:
        st.error("End wavelength must be greater than start wavelength.")

    st.markdown("**Example Temperatures (K)**")
    temp_start = st.number_input("Start temperature (K)", 100, 100000, 3000)
    temp_mid   = st.number_input("Mid temperature (K)", 100, 100000, 6500)
    temp_end   = st.number_input("End temperature (K)", 100, 100000, 10000)

    n_wavelengths = st.slider("Wavelength samples", 50, 1000, 200)
    n_frames = st.slider("3D Animation frames", 10, 240, 60)
    duration = st.slider("3D Frame duration (ms)", 10, 500, 80)
    loop_3d = st.checkbox("Loop 3D animation back & forth", True)

with col_plot:
    st.subheader("3D Animated Blackbody")
    temp_min_3d = min(temp_start, temp_mid, temp_end)
    temp_max_3d = max(temp_start, temp_mid, temp_end)

    fig3d = plot_blackbody_3d_interactive(
        wl_min_nm=wl_min_nm,
        wl_max_nm=wl_max_nm,
        temp_min=temp_min_3d,
        temp_max=temp_max_3d,
        n_wavelengths=n_wavelengths,
        n_frames=n_frames,
        duration=duration,
        loop=loop_3d,
    )
    st.plotly_chart(fig3d, use_container_width=True)

    st.markdown("---")
    if st.button("Show 2D spectra for example temperatures"):
        fig2d, ax = plt.subplots(figsize=(10,4), facecolor="none") 
        fig2d.patch.set_alpha(0)

        wavelengths = np.linspace(wl_min_nm*1e-9, wl_max_nm*1e-9, n_wavelengths)
        example_temps = [temp_start, temp_mid, temp_end]
        colors = ["#FF7F0E", "#1F77B4", "#2CA02C"]

        ax.set_facecolor("none")
        for spine in ax.spines.values():
            spine.set_color('white')
            spine.set_linewidth(1.2)

        ax.tick_params(colors='white', which='both', labelsize=10)
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')

        for T, color in zip(example_temps, colors):
            radiance = planck_law(wavelengths, T)
            ax.plot(wavelengths*1e9, radiance, color=color, lw=2.5, label=f"{T} K")
            ax.fill_between(wavelengths*1e9, 0, radiance, color=color, alpha=0.1)

        ax.set_title("Blackbody Radiation Spectra", fontsize=14, weight='bold')
        ax.set_xlabel("Wavelength (nm)", fontsize=12)
        ax.set_ylabel("Spectral Radiance", fontsize=12)

        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        ax.minorticks_on()
        ax.legend(frameon=True, facecolor="none", edgecolor="white", labelcolor='white')

        st.pyplot(fig2d, use_container_width=True)