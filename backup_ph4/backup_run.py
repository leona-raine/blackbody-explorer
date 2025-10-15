import streamlit as st
from demo_model import (
    plot_blackbody_2d,
    plot_blackbody_3d_interactive,
    plot_blackbody_3d_animated
)
import io

st.set_page_config(layout="wide", page_title="Blackbody Explorer")

st.title("Blackbody Explorer – Planck’s Law in 2D & 3D")

if "view_mode" not in st.session_state:
    st.session_state.view_mode = None

col_controls, col_plot = st.columns([1, 3])

with col_controls:
    st.subheader("Visualization Type")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("📊 3D Surface"):
            st.session_state.view_mode = "surface"
    with c2:
        if st.button("🎞️ 3D Animated"):
            st.session_state.view_mode = "animated"

    st.caption("Select the kind of visualization you want to display.")

    def export_3d_html(fig):
        """Returns HTML string of Plotly figure for download."""
        buffer = io.StringIO()
        fig.write_html(buffer)
        return buffer.getvalue()

    if st.session_state.view_mode in ["surface", "animated"]:
        if st.session_state.view_mode == "surface":
            fig3d = plot_blackbody_3d_interactive([], [0, 1])
            html_label = "📥 Download 3D Surface HTML"
        else:
            fig3d = plot_blackbody_3d_animated()
            html_label = "📥 Download 3D Animated HTML"

        st.download_button(
            label=html_label,
            data=export_3d_html(fig3d),
            file_name="blackbody_3d.html",
            mime="text/html"
        )

    st.markdown("---")

with col_controls:
    st.header("Controls")

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

wl_min_m = wl_min_nm * 1e-9
wl_max_m = wl_max_nm * 1e-9

with col_plot:
    st.subheader("3D Visualization")

    if st.session_state.view_mode == "surface":
        fig3d = plot_blackbody_3d_interactive(example_temps, [wl_min_m, wl_max_m])
        st.plotly_chart(fig3d, use_container_width=True)

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

    else:
        st.info("👈 Choose a visualization type to begin exploring Planck’s Law.")

    st.markdown("---")
    if st.button("📈 Show 2D Spectra for Example Temperatures"):
        fig2d = plot_blackbody_2d(example_temps, wl_min_m, wl_max_m, n_points=n_wavelengths)
        st.pyplot(fig2d, use_container_width=True)

        buf = io.BytesIO()
        fig2d.savefig(buf, format="png", dpi=150)
        buf.seek(0)
        st.download_button(
            label="📥 Download 2D Spectra PNG",
            data=buf,
            file_name="blackbody_2d.png",
            mime="image/png"
        )