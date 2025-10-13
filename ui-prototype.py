import streamlit as st
from phase1 import plot_blackbody_2d, plot_blackbody_3d

st.set_page_config(layout="wide")

# -------------------
# TITLE + PLOT TYPE
# -------------------
col_title, col_plot_type = st.columns([3,1])  # 3:1 ratio for title vs dropdown
with col_title:
    st.title("Blackbody Explorer - Phase 2 UI Lightweight")
with col_plot_type:
    plot_type = st.selectbox("", ["3D", "2D"], key="plot_type", label_visibility="collapsed")

# -------------------
# INPUTS AND PLOTS
# -------------------
col_inputs, col_plot = st.columns([1,2])

with col_inputs:
    # TEMPERATURE INPUTS
    for i, default in enumerate([3000, 3000, 3000], start=1):
        temp_key = f"temp{i}"
        temp_input_key = f"temp{i}_input"

        if temp_key not in st.session_state:
            st.session_state[temp_key] = default
        if temp_input_key not in st.session_state:
            st.session_state[temp_input_key] = default

        def update_slider(i=i):
            st.session_state[f"temp{i}"] = st.session_state[f"temp{i}_input"]
        def update_input(i=i):
            st.session_state[f"temp{i}_input"] = st.session_state[f"temp{i}"]

        st.markdown(f"<b>Temperature {i} (K)</b>", unsafe_allow_html=True)
        c1, c2 = st.columns([1,4])
        with c1:
            st.number_input("", 1000 if i<3 else 3000, 10000,
                            key=temp_input_key, on_change=update_slider)
        with c2:
            st.slider("", 1000 if i<3 else 3000, 10000,
                      key=temp_key, on_change=update_input)

    # WAVELENGTH INPUTS
    for i, (label, default) in enumerate([("Start Wavelength", 380), ("End Wavelength", 750)]):
        key_slider = f"wl_{i}_slider"
        key_input = f"wl_{i}_input"

        if key_slider not in st.session_state:
            st.session_state[key_slider] = default
        if key_input not in st.session_state:
            st.session_state[key_input] = default

        def update_wl_slider(i=i):
            st.session_state[f"wl_{i}_slider"] = st.session_state[f"wl_{i}_input"]
        def update_wl_input(i=i):
            st.session_state[f"wl_{i}_input"] = st.session_state[f"wl_{i}_slider"]

        st.markdown(f"<b>{label} (nm)</b>", unsafe_allow_html=True)
        c1, c2 = st.columns([1,4])
        with c1:
            st.number_input("", 100, 3000, key=key_input, on_change=update_wl_slider)
        with c2:
            st.slider("", 100, 3000, key=key_slider, on_change=update_wl_input)

# -------------------
# PLOTTING
# -------------------
temps = [st.session_state.temp1, st.session_state.temp2, st.session_state.temp3]
wl_range = (st.session_state.wl_0_slider*1e-9, st.session_state.wl_1_slider*1e-9)

with col_plot:
    if plot_type == "3D":
        st.subheader("3D Blackbody Plot")
        fig3d = plot_blackbody_3d(temps, wl_range)
        st.pyplot(fig3d, use_container_width=True)
    else:
        st.subheader("2D Blackbody Plot")
        fig2d = plot_blackbody_2d(temps, wl_range)
        st.pyplot(fig2d, use_container_width=True)