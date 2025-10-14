"""
origin_run.py

Streamlit app that uses interactive_3d.plot_blackbody_3d_interactive
to display a real-time animated 3D blackbody spectrum.

Run:
    streamlit run origin_run.py
"""

import streamlit as st
from interactive_3d import plot_blackbody_2d, plot_blackbody_3d_interactive

st.set_page_config(layout="wide", page_title="Blackbody Explorer 3D")

st.title("Blackbody Explorer – Real-time 3D Animation")

st.markdown(
    "Use the controls on the left to set the wavelength and temperature ranges, "
    "plus animation speed and resolution. Click **▶ Play** to start the animation."
)

# Layout: controls left, plot right
col_controls, col_plot = st.columns([1, 3])

with col_controls:
    st.header("Controls")

    st.markdown("**Wavelength range (nm)**")
    wl_min_nm = st.number_input("Start wavelength (nm)", min_value=10, max_value=20000, value=380, step=1)
    wl_max_nm = st.number_input("End wavelength (nm)", min_value=10, max_value=20000, value=750, step=1)

    if wl_max_nm <= wl_min_nm:
        st.error("End wavelength must be greater than start wavelength.")
    else:
        pass

    st.markdown("**Temperature sweep (K)**")
    temp_min = st.number_input("Min temperature (K)", min_value=100, max_value=100000, value=3000, step=100)
    temp_max = st.number_input("Max temperature (K)", min_value=100, max_value=100000, value=10000, step=100)
    if temp_max <= temp_min:
        st.error("Max temperature must be greater than min temperature.")

    st.markdown("**Animation & resolution**")
    n_wavelengths = st.slider("Wavelength samples", min_value=50, max_value=1000, value=200, step=10)
    n_frames = st.slider("Animation frames (resolution)", min_value=10, max_value=240, value=60, step=1)
    duration = st.slider("Frame duration (ms)", min_value=10, max_value=1000, value=80, step=10)
    loop = st.checkbox("Loop animation (back & forth)", value=True)

    st.markdown("---")
    st.markdown("Tip: After changing sliders, the figure will regenerate. Use the Play button in the figure to run the animation.")

with col_plot:
    # Only compute the figure if inputs valid
    if wl_max_nm <= wl_min_nm or temp_max <= temp_min:
        st.warning("Fix the ranges on the left to generate the animation.")
    else:
        # Cache the heavy figure generation to improve responsiveness
        @st.cache_data(show_spinner=False)
        def build_fig(wl_min_nm, wl_max_nm, temp_min, temp_max, n_wavelengths, n_frames, duration, loop):
            return plot_blackbody_3d_interactive(
                wl_min_nm=wl_min_nm,
                wl_max_nm=wl_max_nm,
                temp_min=temp_min,
                temp_max=temp_max,
                n_wavelengths=n_wavelengths,
                n_frames=n_frames,
                duration=duration,
                loop=loop,
            )

        with st.spinner("Generating animated figure..."):
            fig = build_fig(wl_min_nm, wl_max_nm, temp_min, temp_max, n_wavelengths, n_frames, duration, loop)

        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
        st.caption("Rotate / zoom the 3D view with the mouse. Use Play/Pause buttons to control the animation.")
        # Provide 2D fallback view
        if st.button("Show 2D spectra for example temperatures"):
            sample_temps = [int(temp_min), int((temp_min + temp_max) / 2), int(temp_max)]
            fig2d = plot_blackbody_2d(sample_temps, wl_min_nm * 1e-9, wl_max_nm * 1e-9)
            st.pyplot(fig2d, use_container_width=True)
