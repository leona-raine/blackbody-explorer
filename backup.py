import streamlit as st
from phase1 import plot_blackbody_2d, plot_blackbody_3d

# Wide page
st.set_page_config(layout="wide")
st.title("Blackbody Explorer - Phase 2 UI Lightweight")

# -------------------
# LEFT COLUMN: INPUTS
# -------------------
col_inputs, col_plot = st.columns([1,2])  # left for sliders, right for plot

with col_inputs:
    # -------------------
    # TEMPERATURE INPUTS
    # -------------------
    for i, default in enumerate([3000, 3000, 3000], start=1):
        temp_key = f"temp{i}"
        temp_input_key = f"temp{i}_input"

        if temp_key not in st.session_state:
            st.session_state[temp_key] = default
        if temp_input_key not in st.session_state:
            st.session_state[temp_input_key] = default

        # sync callbacks
        def update_slider(i=i):
            st.session_state[f"temp{i}"] = st.session_state[f"temp{i}_input"]

        def update_input(i=i):
            st.session_state[f"temp{i}_input"] = st.session_state[f"temp{i}"]

        st.write(f"Temperature {i} (K)")
        c1, c2 = st.columns([1,4])
        with c1:
            st.number_input("", 1000 if i<3 else 3000, 10000,
                            key=temp_input_key, on_change=update_slider)
        with c2:
            st.slider("", 1000 if i<3 else 3000, 10000,
                      key=temp_key, on_change=update_input)

    # -------------------
    # WAVELENGTH INPUTS (Below Temperatures)
    # -------------------
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

        st.write(f"{label} (nm)")
        c1, c2 = st.columns([1,4])
        with c1:
            st.number_input("", 100, 3000, key=key_input, on_change=update_wl_slider)
        with c2:
            st.slider("", 100, 3000, key=key_slider, on_change=update_wl_input)

# -------------------
# PLOT SELECTION DROPDOWN
# -------------------
plot_type = st.selectbox("Choose Plot Type:", ["3D", "2D"])

# -------------------
# PLOTTING
# -------------------
temps = [st.session_state.temp1, st.session_state.temp2, st.session_state.temp3]
wl_range = (st.session_state.wl_0_slider*1e-9, st.session_state.wl_1_slider*1e-9)

with col_plot:
    if plot_type == "3D":
        st.subheader("3D Blackbody Plot")
        # Rectangular figure for 3D
        fig3d = plot_blackbody_3d(temps, wl_range)
        fig3d.set_size_inches(8, 6)  # make it rectangular
        st.pyplot(fig3d, use_container_width=True)
    else:
        st.subheader("2D Blackbody Plot")
        fig2d = plot_blackbody_2d(temps, wl_range)
        st.pyplot(fig2d, use_container_width=True)