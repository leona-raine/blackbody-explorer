import streamlit as st
from phase1 import plot_blackbody_2d, plot_blackbody_3d

st.title("Blackbody Explorer - Phase 2 UI Lightweight")

# for temperatures
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

    col1, col2 = st.columns([4,1])
    with col1:
        st.slider(f"Temperature {i} (K)", 1000 if i<3 else 3000, 10000,
                  key=temp_key, on_change=update_input)
    with col2:
        st.number_input(f"", 1000 if i<3 else 3000, 10000,
                        key=temp_input_key, on_change=update_slider)

# for wavelength
# wavelength start
if "wl_start" not in st.session_state:
    st.session_state.wl_start = 380
if "wl_start_input" not in st.session_state:
    st.session_state.wl_start_input = 380

def update_wl_slider():
    st.session_state.wl_start = st.session_state.wl_start_input

def update_wl_input():
    st.session_state.wl_start_input = st.session_state.wl_start

col1, col2 = st.columns([4,1])
with col1:
    st.slider("Start Wavelength (nm)", 100, 3000, key="wl_start", on_change=update_wl_input)
with col2:
    st.number_input("", 100, 3000, key="wl_start_input", on_change=update_wl_slider)

# wavelength end
if "wl_end" not in st.session_state:
    st.session_state.wl_end = 750
if "wl_end_input" not in st.session_state:
    st.session_state.wl_end_input = 750

def update_wl_end_slider():
    st.session_state.wl_end = st.session_state.wl_end_input

def update_wl_end_input():
    st.session_state.wl_end_input = st.session_state.wl_end

col1, col2 = st.columns([4,1])
with col1:
    st.slider("End Wavelength (nm)", 100, 3000, key="wl_end", on_change=update_wl_end_input)
with col2:
    st.number_input("", 100, 3000, key="wl_end_input", on_change=update_wl_end_slider)

# for plotting
temps = [st.session_state.temp1, st.session_state.temp2, st.session_state.temp3]
wl_range = (st.session_state.wl_start*1e-9, st.session_state.wl_end*1e-9)

# create two columns for plots
plot_col1, plot_col2 = st.columns(2)

with plot_col1:
    st.subheader("2D Blackbody Spectrum")
    fig2d = plot_blackbody_2d(temps, wl_range)
    st.pyplot(fig2d, use_container_width=True)

with plot_col2:
    st.subheader("3D Blackbody Spectrum")
    fig3d = plot_blackbody_3d(temps, wl_range)
    st.pyplot(fig3d, use_container_width=True)

