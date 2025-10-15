import pandas as pd
import plotly.io as pio
import io

def export_2d_csv(wavelengths, radiances, temperatures):
    wavelengths_nm = wavelengths * 1e9
    df = pd.DataFrame({"Wavelength (nm)": wavelengths_nm})
    for rad, T in zip(radiances, temperatures):
        df[f"Radiance {T} K"] = rad
    return df.to_csv(index=False).encode('utf-8')

def export_2d_png(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return buf

def export_3d_html(fig):
    buf = io.BytesIO()
    html_str = pio.to_html(fig, include_plotlyjs='cdn')
    buf.write(html_str.encode('utf-8'))
    buf.seek(0)
    return buf