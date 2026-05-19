import numpy as np
import plotly.graph_objects as go

# Parameters
alpha = 0.3
T_bar = 100
T = np.linspace(10, 200, 500)

# MPT function using the mathematically correct Cobb-Douglas derivative
def mpt(T, L, alpha):
    """
    For F(T,L) = T^alpha * L^(1-alpha), 
    the marginal product of land is dF/dT = alpha * (L/T)^(1-alpha)
    """
    return alpha * (L / T)**(1 - alpha)

# We will vary L from 50 to 200
L_values = np.linspace(50, 200, 31)
L_initial = 100

# Fix y-axis maximum so the plot doesn't jump around when moving the slider
y_max = mpt(10, 200, alpha) * 1.05

fig = go.Figure()

# Initial Data (for L = 100)
y_initial = mpt(T, L_initial, alpha)
R_initial = mpt(T_bar, L_initial, alpha)

# 1. Marginal Product of Land (MPT) Curve
fig.add_trace(
    go.Scatter(
        x=T,
        y=y_initial,
        mode='lines',
        name='MPT(T, L)',
        line=dict(color='blue', width=3)
    )
)

# 2. Vertical Land Supply Curve (T_bar)
fig.add_trace(
    go.Scatter(
        x=[T_bar, T_bar],
        y=[0, y_max],
        mode='lines',
        name='Land Supply (T̄)',
        line=dict(color='red', width=3, dash='dash'),
        hoverinfo='skip'
    )
)

# 3. Indicator line for Equilibrium Rental Rate (R)
fig.add_trace(
    go.Scatter(
        x=[0, T_bar],
        y=[R_initial, R_initial],
        mode='lines',
        name='Rental Rate (R)',
        line=dict(color='green', width=2, dash='dot'),
        hoverinfo='skip'
    )
)

# 4. Equilibrium Point
fig.add_trace(
    go.Scatter(
        x=[T_bar],
        y=[R_initial],
        mode='markers',
        name='Equilibrium',
        marker=dict(color='black', size=12),
        hovertemplate='Land (T): %{x}<br>Rental Rate (R): %{y:.2f}<extra></extra>'
    )
)

# Create slider steps for different Labor (L) values
steps = []
for L in L_values:
    y_vals = mpt(T, L, alpha)
    R_val = mpt(T_bar, L, alpha)
    
    step = dict(
        method="update",
        args=[
            {"y": [
                y_vals,            # Update Trace 0 (MPT curve)
                [0, y_max],        # Trace 1 stays same (Vertical line)
                [R_val, R_val],    # Update Trace 2 (Rental Rate horizontal line)
                [R_val]            # Update Trace 3 (Equilibrium point y-coord)
            ]}
        ],
        label=f"{L:.0f}"
    )
    steps.append(step)

# Add the slider to the layout
sliders = [dict(
    active=10, # Index of L=100
    currentvalue={"prefix": "Labor Endowment (L): "},
    pad={"t": 50},
    steps=steps
)]

# Finalize the layout aesthetics
fig.update_layout(
    title='Marginal Product of Land & Equilibrium Rental Rate',
    xaxis_title='Land (T)',
    yaxis_title='Rental Rate / MPT',
    sliders=sliders,
    xaxis=dict(range=[0, 200]),
    yaxis=dict(range=[0, y_max]),
    template='plotly_white',
    legend=dict(x=0.7, y=0.9),
    margin=dict(l=50, r=50, t=80, b=50)
)

# Save plot to an HTML file
output_file = 'mpt_interactive_plot.html'
fig.write_html(output_file)
print(f"Interactive plot successfully saved to {output_file}")
