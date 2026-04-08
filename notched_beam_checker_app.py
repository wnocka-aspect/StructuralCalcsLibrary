import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from math import sqrt, pi

# Page configuration
st.set_page_config(page_title="Notched Beam Section Check", layout="wide", page_icon="🏗️")

st.title("🏗️ Notched Beam Section Check Calculator")
st.markdown("Interactive web app for analyzing composite CLT-Glulam notched beam sections")

# Sidebar for inputs
st.sidebar.header("📐 Input Parameters")

# Geometry Section
st.sidebar.subheader("Composite Section Geometry")
d_tot = st.sidebar.number_input("Overall depth (inches)", value=24.0, min_value=1.0, step=1.0)
w_tot = st.sidebar.number_input("Overall width (inches)", value=22.0, min_value=1.0, step=1.0)
w_bear = st.sidebar.number_input("Bearing notch width each side (inches)", value=5.0, min_value=0.0, step=0.5)
d_CLT = st.sidebar.number_input("CLT panel depth (inches)", value=5.5, min_value=1.0, step=0.5)

# Fire Design Parameters
st.sidebar.subheader("Fire Design Parameters")
t_char = st.sidebar.number_input("Char depth (inches)", value=3.2, min_value=0.0, step=0.1)

# Material Properties
st.sidebar.subheader("Material Properties")
col1, col2 = st.sidebar.columns(2)
with col1:
    f_bp = col1.number_input("f_bp (psi)", value=2400, step=50)
    f_bn = col1.number_input("f_bn (psi)", value=2000, step=50)
    f_vx = col1.number_input("f_vx (psi)", value=300, step=10)
    f_vy = col1.number_input("f_vy (psi)", value=260, step=10)
    f_cpx = col1.number_input("f_cpx (psi)", value=740, step=10)
with col2:
    f_cpy = col2.number_input("f_cpy (psi)", value=650, step=10)
    f_t = col2.number_input("f_t (psi)", value=1150, step=50)
    f_c = col2.number_input("f_c (psi)", value=1650, step=50)
    E_xapp = col2.number_input("E_x (psi)", value=1.8e6, step=1e5, format="%.1e")
    E_yapp = col2.number_input("E_y (psi)", value=1.6e6, step=1e5, format="%.1e")

# Demand
st.sidebar.subheader("Demand (Normal Condition)")
M_max = st.sidebar.number_input("Max moment (lb-ft)", value=218408, step=1000)
V_max = st.sidebar.number_input("Max shear (lb)", value=25232, step=100)

st.sidebar.subheader("Demand (Fire Condition)")
M_max_fire = st.sidebar.number_input("Max moment - Fire (lb-ft)", value=157257, step=1000)
V_max_fire = st.sidebar.number_input("Max shear - Fire (lb)", value=19466, step=100)

# Adjustment Factors
st.sidebar.subheader("Adjustment Factors")
lamb = st.sidebar.number_input("λ (Time effect)", value=0.8, step=0.05)
K_F_b = st.sidebar.number_input("K_F (bending)", value=2.54, step=0.1)
phi_b = st.sidebar.number_input("φ_b (bending)", value=0.85, step=0.05)
C_V = st.sidebar.number_input("C_V (volume factor)", value=0.914, step=0.01)
K_F_v = st.sidebar.number_input("K_F (shear)", value=2.88, step=0.1)
phi_v = st.sidebar.number_input("φ_v (shear)", value=0.75, step=0.05)
C_vr = st.sidebar.number_input("C_vr (shear)", value=1.0, step=0.05)
gamma_b = st.sidebar.number_input("γ_b (fire bending)", value=2.85, step=0.05)
gamma_v = st.sidebar.number_input("γ_v (fire shear)", value=2.75, step=0.05)
C_V_fire = st.sidebar.number_input("C_V (fire)", value=0.914, step=0.01)

# Deflection Parameters
st.sidebar.subheader("Deflection Parameters")
L = st.sidebar.number_input("Span length (ft)", value=30.0, step=1.0)
W_t = st.sidebar.number_input("Tributary width (ft)", value=12.0, step=1.0)
p_SDL = st.sidebar.number_input("Superimposed dead load (psf)", value=36.4, step=1.0)
p_CLT = st.sidebar.number_input("CLT dead load (psf)", value=14.0, step=1.0)
p_L = st.sidebar.number_input("Live load (psf)", value=55.0, step=1.0)
w_SW = st.sidebar.number_input("Beam self-weight (lb/ft)", value=133.0, step=1.0)
k_creep = st.sidebar.number_input("Creep factor", value=1.5, step=0.1)
Delta_Lmax = st.sidebar.number_input("L/Δ_L limit", value=480, step=10)
Delta_DLmax = st.sidebar.number_input("L/Δ_DL limit", value=240, step=10)

# ============ CALCULATIONS ============

# Transformed Section Properties
b_low = w_tot
h_low = d_tot - d_CLT
A_low = b_low * h_low
b_hi = w_tot - 2 * w_bear
h_hi = d_CLT
A_hi = b_hi * h_hi
A_net = A_low + A_hi

# Moment of Inertia
y_bar = (A_low * h_low / 2 + A_hi * (d_tot - h_hi / 2)) / A_net
delta_low = abs(y_bar - h_low / 2)
delta_hi = abs(d_tot - y_bar - h_hi / 2)
I_low = b_low * h_low**3 / 12
I_hi = b_hi * h_hi**3 / 12
I_tot = I_low + A_low * delta_low**2 + I_hi + A_hi * delta_hi**2

# Fire Case Transformed Section Properties
b_low_fire = b_low - 2 * t_char
h_low_fire = h_low - t_char
A_low_fire = b_low_fire * h_low_fire
A_net_fire = A_low_fire + A_hi

# Moment of Inertia (Fire)
y_bar_fire = (A_low_fire * h_low_fire / 2 + A_hi * (h_low_fire + h_hi / 2)) / A_net_fire
delta_low_fire = abs(y_bar_fire - h_low_fire / 2)
delta_hi_fire = abs(h_low_fire + h_hi / 2 - y_bar_fire)
I_low_fire = b_low_fire * h_low_fire**3 / 12
I_hi_fire = b_hi * h_hi**3 / 12
I_tot_fire = I_low_fire + A_low_fire * delta_low_fire**2 + I_hi_fire + A_hi * delta_hi_fire**2

# Convert moment to lb-in
M_max_in = M_max * 12
M_max_fire_in = M_max_fire * 12

# Bending Strength Check
S_x = I_tot / max(y_bar, d_tot - y_bar)
f_br = M_max_in / S_x
f_prime_b = f_bp * lamb * K_F_b * C_V * phi_b
U_b = f_br / f_prime_b

# Shear Strength Check
f_vr = 3 * V_max / (2 * b_hi * d_tot)
f_prime_v = f_vx * K_F_v * C_vr * phi_v
U_v = f_vr / f_prime_v

# Bending Strength Check (Fire)
S_x_fire = I_tot_fire / max(y_bar_fire, h_low_fire + h_hi - y_bar_fire)
f_br_fire = M_max_fire_in / S_x_fire
f_prime_b_fire = f_bp * gamma_b * C_V_fire
U_b_fire = f_br_fire / f_prime_b_fire

# Shear Strength Check (Fire)
f_vr_fire = 3 * V_max_fire / (2 * b_hi * d_tot)
f_prime_v_fire = f_vx * gamma_v * C_vr * phi_v
U_v_fire = f_vr_fire / f_prime_v_fire

# Deflection Checks
L_in = L * 12
w_D = (W_t * (p_SDL + p_CLT) + w_SW) / 12  # Convert lb/ft to lb/in
w_L = (W_t * p_L) / 12  # Convert lb/ft to lb/in

delta_L = (5 * w_L * (L_in)**4) / (384 * E_xapp * I_tot)
Delta_L = L_in / delta_L
U_Delta_L = Delta_Lmax / Delta_L

delta_DL = (5 * (k_creep * w_D + w_L) * (L_in)**4) / (384 * E_xapp * I_tot)
Delta_DL = L_in / delta_DL
U_Delta_DL = Delta_DLmax / Delta_DL

# ============ DISPLAY RESULTS ============

# Create tabs for organization
tab1, tab2, tab3, tab4 = st.tabs(["📊 Utilization Summary", "📈 Visual Results", "🔢 Section Properties", "📄 Detailed Calculations"])

with tab1:
    st.header("Utilization Ratios (U)")
    st.markdown("*Utilization ratio U = Demand / Capacity. **U < 1.0 = PASS** ✅ | U ≥ 1.0 = FAIL ❌*")
    
    # Create utilization dataframe
    u_data = {
        'Check': [
            'Bending (Normal)',
            'Shear (Normal)',
            'Bending (Fire)',
            'Shear (Fire)',
            'Deflection (Live Load)',
            'Deflection (Total Load)'
        ],
        'Utilization (U)': [U_b, U_v, U_b_fire, U_v_fire, U_Delta_L, U_Delta_DL],
        'Status': [
            '✅ PASS' if U_b < 1.0 else '❌ FAIL',
            '✅ PASS' if U_v < 1.0 else '❌ FAIL',
            '✅ PASS' if U_b_fire < 1.0 else '❌ FAIL',
            '✅ PASS' if U_v_fire < 1.0 else '❌ FAIL',
            '✅ PASS' if U_Delta_L < 1.0 else '❌ FAIL',
            '✅ PASS' if U_Delta_DL < 1.0 else '❌ FAIL'
        ],
        'Demand': [
            f"{f_br:.1f} psi",
            f"{f_vr:.1f} psi",
            f"{f_br_fire:.1f} psi",
            f"{f_vr_fire:.1f} psi",
            f"L/{Delta_L:.0f}",
            f"L/{Delta_DL:.0f}"
        ],
        'Capacity': [
            f"{f_prime_b:.1f} psi",
            f"{f_prime_v:.1f} psi",
            f"{f_prime_b_fire:.1f} psi",
            f"{f_prime_v_fire:.1f} psi",
            f"L/{Delta_Lmax}",
            f"L/{Delta_DLmax}"
        ]
    }
    
    df_u = pd.DataFrame(u_data)
    
    # Display as styled dataframe
    def color_status(val):
        if '✅' in val:
            return 'background-color: #d4edda; color: #155724'
        elif '❌' in val:
            return 'background-color: #f8d7da; color: #721c24'
        return ''
    
    styled_df = df_u.style.map(color_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True, height=280)
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    max_u = max(U_b, U_v, U_b_fire, U_v_fire, U_Delta_L, U_Delta_DL)
    passes = sum([U_b < 1.0, U_v < 1.0, U_b_fire < 1.0, U_v_fire < 1.0, U_Delta_L < 1.0, U_Delta_DL < 1.0])
    
    col1.metric("Maximum U", f"{max_u:.3f}", 
                delta=f"{(max_u - 1.0):.3f}", 
                delta_color="inverse")
    col2.metric("Checks Passed", f"{passes}/6")
    col3.metric("Overall Status", "✅ PASS" if passes == 6 else "❌ FAIL")

with tab2:
    st.header("Visual Analysis")
    
    # Create bar chart for utilization ratios
    fig = go.Figure()
    
    colors = ['#28a745' if u < 1.0 else '#dc3545' for u in [U_b, U_v, U_b_fire, U_v_fire, U_Delta_L, U_Delta_DL]]
    
    fig.add_trace(go.Bar(
        x=[U_b, U_v, U_b_fire, U_v_fire, U_Delta_L, U_Delta_DL],
        y=['Bending', 'Shear', 'Bending (Fire)', 'Shear (Fire)', 'Deflection (L)', 'Deflection (D+L)'],
        orientation='h',
        marker=dict(color=colors),
        text=[f'{u:.3f}' for u in [U_b, U_v, U_b_fire, U_v_fire, U_Delta_L, U_Delta_DL]],
        textposition='outside'
    ))
    
    fig.add_vline(x=1.0, line_dash="dash", line_color="red", annotation_text="Limit (U=1.0)")
    
    fig.update_layout(
        title="Utilization Ratios",
        xaxis_title="Utilization (U)",
        yaxis_title="Check Type",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Cross-section visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Normal Condition Cross-Section")
        fig_section = go.Figure()
        
        # Lower section (full width)
        fig_section.add_trace(go.Scatter(
            x=[0, b_low, b_low, 0, 0],
            y=[0, 0, h_low, h_low, 0],
            fill='toself',
            fillcolor='lightblue',
            line=dict(color='blue', width=2),
            name='Glulam',
            hovertemplate='Lower section (Glulam)<br>Width: %.1f in<br>Height: %.1f in<extra></extra>' % (b_low, h_low)
        ))
        
        # Upper section (reduced width)
        x_offset = w_bear
        fig_section.add_trace(go.Scatter(
            x=[x_offset, x_offset + b_hi, x_offset + b_hi, x_offset, x_offset],
            y=[h_low, h_low, d_tot, d_tot, h_low],
            fill='toself',
            fillcolor='lightyellow',
            line=dict(color='orange', width=2),
            name='CLT',
            hovertemplate='Upper section (CLT)<br>Width: %.1f in<br>Height: %.1f in<extra></extra>' % (b_hi, h_hi)
        ))
        
        # Neutral axis
        fig_section.add_hline(y=y_bar, line_dash="dash", line_color="red", 
                             annotation_text=f"NA: {y_bar:.2f} in")
        
        fig_section.update_layout(
            height=500,
            xaxis_title="Width (in)",
            yaxis_title="Height (in)",
            showlegend=True,
            yaxis=dict(scaleanchor="x", scaleratio=1)
        )
        
        st.plotly_chart(fig_section, use_container_width=True)
    
    with col2:
        st.subheader("Fire Condition Cross-Section")
        fig_fire = go.Figure()
        
        # Lower section (reduced)
        fig_fire.add_trace(go.Scatter(
            x=[t_char, t_char + b_low_fire, t_char + b_low_fire, t_char, t_char],
            y=[0, 0, h_low_fire, h_low_fire, 0],
            fill='toself',
            fillcolor='lightcoral',
            line=dict(color='darkred', width=2),
            name='Glulam (reduced)',
            hovertemplate='Lower section (Fire)<br>Width: %.1f in<br>Height: %.1f in<extra></extra>' % (b_low_fire, h_low_fire)
        ))
        
        # Upper section (unchanged)
        x_offset = w_bear
        fig_fire.add_trace(go.Scatter(
            x=[x_offset, x_offset + b_hi, x_offset + b_hi, x_offset, x_offset],
            y=[h_low_fire, h_low_fire, h_low_fire + h_hi, h_low_fire + h_hi, h_low_fire],
            fill='toself',
            fillcolor='lightyellow',
            line=dict(color='orange', width=2),
            name='CLT',
            hovertemplate='Upper section (CLT)<br>Width: %.1f in<br>Height: %.1f in<extra></extra>' % (b_hi, h_hi)
        ))
        
        # Neutral axis
        fig_fire.add_hline(y=y_bar_fire, line_dash="dash", line_color="red",
                          annotation_text=f"NA: {y_bar_fire:.2f} in")
        
        fig_fire.update_layout(
            height=500,
            xaxis_title="Width (in)",
            yaxis_title="Height (in)",
            showlegend=True,
            yaxis=dict(scaleanchor="x", scaleratio=1)
        )
        
        st.plotly_chart(fig_fire, use_container_width=True)

with tab3:
    st.header("Section Properties")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Normal Condition")
        props_normal = {
            'Property': [
                'Lower width (b_low)',
                'Lower height (h_low)',
                'Lower area (A_low)',
                'Upper width (b_hi)',
                'Upper height (h_hi)',
                'Upper area (A_hi)',
                'Net area (A_net)',
                'Centroid (y_bar)',
                'Moment of Inertia (I_tot)',
                'Section Modulus (S_x)'
            ],
            'Value': [
                f'{b_low:.2f} in',
                f'{h_low:.2f} in',
                f'{A_low:.2f} in²',
                f'{b_hi:.2f} in',
                f'{h_hi:.2f} in',
                f'{A_hi:.2f} in²',
                f'{A_net:.2f} in²',
                f'{y_bar:.2f} in',
                f'{I_tot:.0f} in⁴',
                f'{S_x:.1f} in³'
            ]
        }
        st.dataframe(pd.DataFrame(props_normal), use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("Fire Condition")
        props_fire = {
            'Property': [
                'Lower width (b_low_fire)',
                'Lower height (h_low_fire)',
                'Lower area (A_low_fire)',
                'Upper width (b_hi)',
                'Upper height (h_hi)',
                'Upper area (A_hi)',
                'Net area (A_net_fire)',
                'Centroid (y_bar_fire)',
                'Moment of Inertia (I_tot_fire)',
                'Section Modulus (S_x_fire)'
            ],
            'Value': [
                f'{b_low_fire:.2f} in',
                f'{h_low_fire:.2f} in',
                f'{A_low_fire:.2f} in²',
                f'{b_hi:.2f} in',
                f'{h_hi:.2f} in',
                f'{A_hi:.2f} in²',
                f'{A_net_fire:.2f} in²',
                f'{y_bar_fire:.2f} in',
                f'{I_tot_fire:.0f} in⁴',
                f'{S_x_fire:.1f} in³'
            ]
        }
        st.dataframe(pd.DataFrame(props_fire), use_container_width=True, hide_index=True)

with tab4:
    st.header("Detailed Calculations")
    
    st.subheader("Bending Checks")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Normal Condition**")
        st.latex(r'f_{br} = \frac{M_{max}}{S_x} = \frac{%.0f \text{ lb-in}}{%.1f \text{ in}^3} = %.1f \text{ psi}' % (M_max_in, S_x, f_br))
        st.latex(r"f'_b = f_{bp} \cdot \lambda \cdot K_F \cdot C_V \cdot \phi_b = %.1f \text{ psi}" % f_prime_b)
        st.latex(r'U_b = \frac{%.1f}{%.1f} = %.3f' % (f_br, f_prime_b, U_b))
    
    with col2:
        st.markdown("**Fire Condition**")
        st.latex(r'f_{br,fire} = \frac{M_{max,fire}}{S_{x,fire}} = %.1f \text{ psi}' % f_br_fire)
        st.latex(r"f'_{b,fire} = f_{bp} \cdot \gamma_b \cdot C_V = %.1f \text{ psi}" % f_prime_b_fire)
        st.latex(r'U_{b,fire} = \frac{%.1f}{%.1f} = %.3f' % (f_br_fire, f_prime_b_fire, U_b_fire))
    
    st.subheader("Shear Checks")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Normal Condition**")
        st.latex(r'f_{vr} = \frac{3V_{max}}{2b_{hi}d_{tot}} = %.1f \text{ psi}' % f_vr)
        st.latex(r"f'_v = f_{vx} \cdot K_F \cdot C_{vr} \cdot \phi_v = %.1f \text{ psi}" % f_prime_v)
        st.latex(r'U_v = \frac{%.1f}{%.1f} = %.3f' % (f_vr, f_prime_v, U_v))
    
    with col2:
        st.markdown("**Fire Condition**")
        st.latex(r'f_{vr,fire} = \frac{3V_{max,fire}}{2b_{hi}d_{tot}} = %.1f \text{ psi}' % f_vr_fire)
        st.latex(r"f'_{v,fire} = f_{vx} \cdot \gamma_v \cdot C_{vr} \cdot \phi_v = %.1f \text{ psi}" % f_prime_v_fire)
        st.latex(r'U_{v,fire} = \frac{%.1f}{%.1f} = %.3f' % (f_vr_fire, f_prime_v_fire, U_v_fire))
    
    st.subheader("Deflection Checks")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Live Load Only**")
        st.latex(r'\delta_L = \frac{5w_LL^4}{384EI} = %.3f \text{ in}' % delta_L)
        st.latex(r'\Delta_L = \frac{L}{\delta_L} = \frac{%.0f}{%.3f} = %.0f' % (L_in, delta_L, Delta_L))
        st.latex(r'U_{\Delta_L} = \frac{%d}{%.0f} = %.3f' % (Delta_Lmax, Delta_L, U_Delta_L))
    
    with col2:
        st.markdown("**Total Load**")
        st.latex(r'\delta_{DL} = \frac{5(k_{creep} \cdot w_D + w_L)L^4}{384EI} = %.3f \text{ in}' % delta_DL)
        st.latex(r'\Delta_{DL} = \frac{L}{\delta_{DL}} = %.0f' % Delta_DL)
        st.latex(r'U_{\Delta_{DL}} = \frac{%d}{%.0f} = %.3f' % (Delta_DLmax, Delta_DL, U_Delta_DL))

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit | Notched Beam Section Check Calculator*")
