import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

st.set_page_config(layout="wide", page_title="Malthusian Dynamics Model")

st.title("Malthusian Dynamics")
st.markdown("### ECO 331 Economic History (Conning)")

st.markdown("""
Population $N$ and income $Y$ are related by the following system of differential equations:

$\\frac{dN}{dt} = N \cdot (b(y) - d(y))$

$\\frac{dY}{dt} = g - cN$

where:
- $y = \\frac{Y}{N}$ (per capita resources)
- $b(y) = b_0y$ (birth rate increases linearly with resources)
- $d(y) = d_0e^{-\\alpha y}$ (death rate decreases exponentially with resources)
""")

# Sidebar for inputs
st.sidebar.header("Model Parameters")
b0_val = st.sidebar.slider("Base birth rate (b0)", min_value=0.05, max_value=1.0, value=0.7, step=0.01)
d0_val = st.sidebar.slider("Base death rate (d0)", min_value=0.05, max_value=1.0, value=0.15, step=0.01)
alpha_val = st.sidebar.slider("Sensitivity to resources (alpha)", min_value=0.1, max_value=1.0, value=0.2, step=0.1)
g_val = st.sidebar.slider("Resource growth rate (g)", min_value=0.0, max_value=120.0, value=100.0, step=1.0)
c_val = st.sidebar.slider("Resource consumption rate (c)", min_value=0.0, max_value=0.2, value=0.1, step=0.001)


def plot_both(b0, d0, alpha, g, c):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Left plot - Birth and Death rates
    y = np.linspace(0, 1, 100)
    birth_rate = b0 * y
    death_rate = d0 * np.exp(-alpha * y)

    ax1.plot(y, birth_rate, 'b-', label=r'$b(y) = b_0 y$')
    ax1.plot(y, death_rate, 'r-', label=r'$d(y) = d_0 e^{-\alpha y}$', alpha=0.7) 

    # Find intersection
    intersections = np.abs(birth_rate - death_rate)
    intersection_idx = np.argmin(intersections)
    y_equilibrium = y[intersection_idx]
    rate_equilibrium = birth_rate[intersection_idx]

    ax1.plot(y_equilibrium, rate_equilibrium, 'ko', label=f'Equilibrium at y ≈ {y_equilibrium:.2f}')

    ax1.set_xlabel('Per capita resources (y = Y/N)')
    ax1.set_ylabel('Rate')
    ax1.set_title('Birth and Death Rates')
    ax1.set_ylim(0, 1.5)  
    ax1.grid(True)
    ax1.legend()

    # Right plot - Population dynamics
    def dynamics(state, t, b0, d0, alpha, g, c):
        N, Y = state
        r = Y/N if N > 0 else Y
        birth_rate = b0 * r
        death_rate = d0 * np.exp(-alpha * r)
        dNdt = N * (birth_rate - death_rate)
        dYdt = g - c*N
        return [dNdt, dYdt]

    t = np.linspace(0, 100, 1000)
    N0, Y0 = 1.0, 2.0
    state0 = [N0, Y0]

    solution = odeint(dynamics, state0, t, args=(b0, d0, alpha, g, c))

    ax2_twin = ax2.twinx()

    pop_line = ax2.plot(t, solution[:, 0], 'b-', label='Population')[0]
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Population (N)', color='b')
    ax2.tick_params(axis='y', labelcolor='b')
    ax2.set_ylim(0, 1400)

    per_capita = solution[:, 1] / solution[:, 0]
    res_line = ax2_twin.plot(t, per_capita, 'r-', label='Per capita resources')[0]

    ax2_twin.axhline(y=y_equilibrium, color='k', linestyle='--', label=f'Equilibrium (r = {y_equilibrium:.2f})')

    ax2_twin.set_ylabel('Per capita resources (Y/N)', color='r')
    ax2_twin.tick_params(axis='y', labelcolor='r')
    ax2_twin.set_ylim(0, 1)

    lines = [pop_line, res_line]
    labels = [l.get_label() for l in lines]
    ax2.legend(lines, labels, loc='upper right')

    ax2.grid(True)

    plt.tight_layout()
    return fig

# Render plot
fig = plot_both(b0=b0_val, d0=d0_val, alpha=alpha_val, g=g_val, c=c_val)
st.pyplot(fig)
