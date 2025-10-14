import streamlit as st
from demo_model import plot_blackbody_2d, plot_blackbody_3d_interactive

st.set_page_config(layout="wide", page_title="Blackbody Explorer 3D")

st.title("Blackbody Explorer – Real-time 3D Animation")

st.markdown(
    "Use the controls on the left to set the wavelength and temperature ranges, "
    "plus animation speed and resolution. Click **▶ Play** to start the animation."
)

col_controls, col_plot = st.columns([1, 3])

with col_controls:
    st.header("Controls")

    wl_min_nm = st.number_input("Start wavelength (nm)", min_value=10, max_value=20000, value=380, step=1)
    wl_max_nm = st.number_input("End wavelength (nm)", min_value=10, max_value=20000, value=750, step=1)
    if wl_max_nm <= wl_min_nm:
        st.error("End wavelength must be greater than start wavelength.")

    temp_min = st.number_input("Min temperature (K)", min_value=100, max_value=100000, value=3000, step=100)
    temp_max = st.number_input("Max temperature (K)", min_value=100, max_value=100000, value=10000, step=100)
    if temp_max <= temp_min:
        st.error("Max temperature must be greater than min temperature.")

    n_wavelengths = st.slider("Wavelength samples", min_value=50, max_value=1000, value=200, step=10)
    n_frames = st.slider("Animation frames (resolution)", min_value=10, max_value=240, value=60, step=1)
    duration = st.slider("Frame duration (ms)", min_value=10, max_value=1000, value=80, step=10)
    loop = st.checkbox("Loop animation (back & forth)", value=True)

if wl_max_nm > wl_min_nm and temp_max > temp_min:

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

    with st.spinner("Generating animated 3D figure..."):
        fig3d = build_fig(wl_min_nm, wl_max_nm, temp_min, temp_max, n_wavelengths, n_frames, duration, loop)

    with col_plot:
        st.subheader("3D Animated Blackbody Spectrum")
        st.plotly_chart(fig3d, use_container_width=True, theme="streamlit")
        st.caption("Rotate / zoom the 3D view. Use Play/Pause buttons to control animation.")

        st.subheader("2D Blackbody Spectrum (synchronized)")

        temp_choice = st.radio(
            "Select temperature to show in 2D plot:",
            ("Start temperature", "Mid temperature", "End temperature")
        )

        if temp_choice == "Start temperature":
            temp_2d = temp_min
        elif temp_choice == "Mid temperature":
            temp_2d = (temp_min + temp_max) / 2
        else:
            temp_2d = temp_max

        fig2d = plot_blackbody_2d([temp_2d], wl_min_nm*1e-9, wl_max_nm*1e-9)
        st.pyplot(fig2d, use_container_width=True)