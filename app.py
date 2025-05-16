import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Konfigurasi simbolik
x, y = sp.symbols('x y')

st.title("Aplikasi Turunan Parsial dan Visualisasi 3D")
st.markdown("Masukkan fungsi dua variabel f(x, y) dan titik (x0, y0) untuk menghitung turunan parsial serta menampilkan grafik.")

# Input dari pengguna
fungsi_input = st.text_input("Masukkan fungsi f(x, y):", value="x**2 + y**2")
x0 = st.number_input("Masukkan nilai x0:", value=1.0)
y0 = st.number_input("Masukkan nilai y0:", value=1.0)

try:
    # Parsing fungsi
    f = sp.sympify(fungsi_input)
    fx = sp.diff(f, x)
    fy = sp.diff(f, y)

    # Evaluasi turunan di titik (x0, y0)
    fx_val = fx.evalf(subs={x: x0, y: y0})
    fy_val = fy.evalf(subs={x: x0, y: y0})

    st.latex(f"f_x = {sp.latex(fx)}, \\quad f_y = {sp.latex(fy)}")
    st.write(f"Nilai f_x({x0}, {y0}) = {fx_val}")
    st.write(f"Nilai f_y({x0}, {y0}) = {fy_val}")

    # Konversi fungsi ke fungsi numerik
    f_lambd = sp.lambdify((x, y), f, 'numpy')

    # Data untuk plot 3D
    X = np.linspace(x0 - 2, x0 + 2, 50)
    Y = np.linspace(y0 - 2, y0 + 2, 50)
    X, Y = np.meshgrid(X, Y)
    Z = f_lambd(X, Y)

    # Bidang singgung z = f(x0, y0) + fx*(x - x0) + fy*(y - y0)
    z0 = f.evalf(subs={x: x0, y: y0})
    Z_tangent = float(z0) + float(fx_val)*(X - x0) + float(fy_val)*(Y - y0)

    # Plotting
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, alpha=0.7, cmap='viridis', label='Fungsi')
    ax.plot_surface(X, Y, Z_tangent, alpha=0.5, color='red')

    ax.set_title("Permukaan Fungsi dan Bidang Singgung")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    st.pyplot(fig)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
