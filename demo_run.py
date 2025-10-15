import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from demo_model import (
    plot_blackbody_2d,
    plot_blackbody_3d_interactive,
    plot_blackbody_3d_animated
)
import io

st.set_page_config(layout="wide", page_title="Blackbody Explorer")

st.title("Blackbody Explorer – Planck’s Law in 2D & 3D")

# Initialize session state
if "view_mode" not in st.session_state:
    st.session_state.view_mode = None

# --------------------------
# Layout: Controls & Plot
# --------------------------
col_controls, col_plot = st.columns([1, 3])

with col_controls:
    st.subheader("Visualization Type")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("📊 3D Surface"):
            st.session_state.view_mode = "surface"
    with c2:
        if st.button("🎞️ 3D Animated"):
            st.session_state.view_mode = "animated"
    with c3:
        if st.button("📈 2D Spectra"):
            st.session_state.view_mode = "2d"

    st.caption("Select the kind of visualization you want to display.")

    st.markdown("---")
    st.header("Controls")

    # --------------------------
    # Wavelength & Temperatures
    # --------------------------
    wl_min_nm = st.number_input("Start wavelength (nm)", min_value=10, max_value=20000, value=380, step=10)
    wl_max_nm = st.number_input("End wavelength (nm)", min_value=10, max_value=20000, value=750, step=10)
    if wl_max_nm <= wl_min_nm:
        st.error("⚠️ End wavelength must be greater than start wavelength.")

    st.markdown("**Example Temperatures (Kelvin)**")
    temp_1 = st.number_input("Temperature 1 (K)", min_value=100, max_value=100000, value=3000, step=100)
    temp_2 = st.number_input("Temperature 2 (K)", min_value=100, max_value=100000, value=6500, step=100)
    temp_3 = st.number_input("Temperature 3 (K)", min_value=100, max_value=100000, value=10000, step=100)

    example_temps = sorted([temp_1, temp_2, temp_3])
    st.caption(f"Sorted order → {example_temps[0]} K < {example_temps[1]} K < {example_temps[2]} K")

    st.markdown("**3D Animation Parameters**")
    n_wavelengths = st.slider("Wavelength samples", 50, 1000, 200)
    n_frames = st.slider("3D Animation frames", 10, 240, 60)
    duration = st.slider("3D Frame duration (ms)", 10, 500, 80)
    loop_3d = st.checkbox("Loop 3D animation back & forth", value=True)

    st.markdown("---")
    if st.button("🧹 Reset Visualization"):
        st.session_state.view_mode = None

# --------------------------
# Precompute / conversions
# --------------------------
wl_min_m = wl_min_nm * 1e-9
wl_max_m = wl_max_nm * 1e-9

# --------------------------
# 3D & 2D Visualization
# --------------------------
with col_plot:
    st.subheader("Visualization Output")

    if st.session_state.view_mode == "surface":
        fig3d = plot_blackbody_3d_interactive(example_temps, [wl_min_m, wl_max_m])
        st.plotly_chart(fig3d, use_container_width=True)
        html_label = "📥 Download 3D Surface HTML"

    elif st.session_state.view_mode == "animated":
        fig3d = plot_blackbody_3d_animated(
            wl_min_nm=wl_min_nm,
            wl_max_nm=wl_max_nm,
            temp_min=example_temps[0],
            temp_max=example_temps[-1],
            n_wavelengths=n_wavelengths,
            n_frames=n_frames,
            duration=duration,
            loop=loop_3d,
        )
        st.plotly_chart(fig3d, use_container_width=True)
        html_label = "📥 Download 3D Animated HTML"

    elif st.session_state.view_mode == "2d":
        fig2d = plot_blackbody_2d(example_temps, wl_min_m, wl_max_m, n_points=n_wavelengths)
        st.pyplot(fig2d, use_container_width=True)

        def export_2d_png(fig):
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=150)
            buf.seek(0)
            return buf

        st.download_button(
            label="📥 Download 2D Spectra PNG",
            data=export_2d_png(fig2d),
            file_name="blackbody_2d.png",
            mime="image/png"
        )
        html_label = None

    else:
        st.info("👈 Choose a visualization type to begin exploring Planck’s Law.")

    # 3D HTML download button
    if st.session_state.view_mode in ["surface", "animated"]:
        def export_3d_html(fig):
            buffer = io.StringIO()
            fig.write_html(buffer)
            return buffer.getvalue()

        st.download_button(
            label=html_label,
            data=export_3d_html(fig3d),
            file_name="blackbody_3d.html",
            mime="text/html"
        )
