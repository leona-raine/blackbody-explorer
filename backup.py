import streamlit as st
from phase1 import plot_blackbody_2d, plot_blackbody_3d

st.title("Blackbody Explorer - Phase 2 UI Lightweight")

# -------------------
# TEMPERATURE INPUTS
# -------------------
temps = []
for i, default in enumerate([3000, 3000, 3000], start=1):
    temp_key = f"temp{i}"
    temp_input_key = f"temp{i}_input"

    if temp_key not in st.session_state:
        st.session_state[temp_key] = default
    if temp_input_key not in st.session_state:
        st.session_state[temp_input_key] = default

    # Sync callbacks
    def update_slider(i=i):
        st.session_state[f"temp{i}"] = st.session_state[f"temp{i}_input"]

    def update_input(i=i):
        st.session_state[f"temp{i}_input"] = st.session_state[f"temp{i}"]

    st.write(f"Temperature {i} (K)")
    col1, col2 = st.columns([1, 4])
    with col1:
        st.number_input("", 1000 if i < 3 else 3000, 10000,
                        key=temp_input_key, on_change=update_slider)
    with col2:
        st.slider("", 1000 if i < 3 else 3000, 10000,
                  key=temp_key, on_change=update_input)

# -------------------
# WAVELENGTH INPUTS
# -------------------
# Start wavelength
if "wl_start" not in st.session_state:
    st.session_state.wl_start = 380
if "wl_start_input" not in st.session_state:
    st.session_state.wl_start_input = 380

def update_wl_slider():
    st.session_state.wl_start = st.session_state.wl_start_input

def update_wl_input():
    st.session_state.wl_start_input = st.session_state.wl_start

st.write("Start Wavelength (nm)")
col1, col2 = st.columns([1,4])
with col1:
    st.number_input("", 100, 3000, key="wl_start_input", on_change=update_wl_slider)
with col2:
    st.slider("", 100, 3000, key="wl_start", on_change=update_wl_input)

# End wavelength
if "wl_end" not in st.session_state:
    st.session_state.wl_end = 750
if "wl_end_input" not in st.session_state:
    st.session_state.wl_end_input = 750

def update_wl_end_slider():
    st.session_state.wl_end = st.session_state.wl_end_input

def update_wl_end_input():
    st.session_state.wl_end_input = st.session_state.wl_end

st.write("End Wavelength (nm)")
col1, col2 = st.columns([1,4])
with col1:
    st.number_input("", 100, 3000, key="wl_end_input", on_change=update_wl_end_slider)
with col2:
    st.slider("", 100, 3000, key="wl_end", on_change=update_wl_end_input)

# -------------------
# PLOTTING SIDE
# -------------------
temps = [st.session_state.temp1, st.session_state.temp2, st.session_state.temp3]
wl_range = (st.session_state.wl_start*1e-9, st.session_state.wl_end*1e-9)

# Put 2D and 3D plots side by side
col_plot1, col_plot2 = st.columns([1,1])

with col_plot1:
    fig2d = plot_blackbody_2d(temps, wl_range)
    st.pyplot(fig2d)

with col_plot2:
    fig3d = plot_blackbody_3d(temps, wl_range)
    st.pyplot(fig3d)