import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow
import pandas as pd

# Konfigurasjon
st.set_page_config(
    page_title="Geoteknisk Bæreevneanalyse",
    page_icon="🏗️",
    layout="wide"
)

# Tittel
st.title("🏗️ Geoteknisk Bæreevneanalyse")
st.markdown("*Beregning av fundamenters bæreevne etter Eurocode 7*")
st.divider()

# Sidebar - Input parametere
st.sidebar.header("📊 Inndata")

st.sidebar.subheader("Grunnforhold")
phi_k = st.sidebar.number_input(
    "Karakteristisk friksjonsvinkel φ'k (°)",
    min_value=15.0,
    max_value=45.0,
    value=30.0,
    step=0.5,
    help="Friksjonsvinkel for jord"
)

c_k = st.sidebar.number_input(
    "Attraksjon c'k (kN/m²)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=1.0,
    help="Kohesjon/attraksjon i jord"
)

gamma = st.sidebar.number_input(
    "Romvekt γ (kN/m³)",
    min_value=15.0,
    max_value=25.0,
    value=18.0,
    step=0.5,
    help="Effektiv romvekt av jord"
)

st.sidebar.subheader("Materialfaktorer (EC7)")
gamma_phi = st.sidebar.number_input(
    "Materialfaktor for φ' (γφ')",
    min_value=1.0,
    max_value=1.5,
    value=1.25,
    step=0.05,
    help="Typisk 1.25 for DA2 eller DA3"
)

gamma_c = st.sidebar.number_input(
    "Materialfaktor for c' (γc')",
    min_value=1.0,
    max_value=1.5,
    value=1.25,
    step=0.05,
    help="Typisk 1.25 for DA2 eller DA3"
)

st.sidebar.subheader("Fundamentgeometri")
B = st.sidebar.number_input(
    "Bredde B (m)",
    min_value=0.5,
    max_value=10.0,
    value=2.0,
    step=0.1,
    help="Fundamentbredde"
)

L = st.sidebar.number_input(
    "Lengde L (m)",
    min_value=0.5,
    max_value=20.0,
    value=2.0,
    step=0.1,
    help="Fundamentlengde (L >> B for stripefundament)"
)

D = st.sidebar.number_input(
    "Fundamentdybde D (m)",
    min_value=0.0,
    max_value=5.0,
    value=1.0,
    step=0.1,
    help="Dybde fra terreng til fundamentunderkant"
)

st.sidebar.subheader("Laster")
V_k = st.sidebar.number_input(
    "Karakteristisk vertikallast Vk (kN)",
    min_value=0.0,
    max_value=10000.0,
    value=400.0,
    step=10.0,
    help="Total vertikallast på fundamentet"
)

H_k = st.sidebar.number_input(
    "Karakteristisk horisontallast Hk (kN)",
    min_value=0.0,
    max_value=1000.0,
    value=0.0,
    step=5.0,
    help="Horisontallast (valgfri)"
)

M_k = st.sidebar.number_input(
    "Karakteristisk moment Mk (kNm)",
    min_value=0.0,
    max_value=5000.0,
    value=0.0,
    step=10.0,
    help="Moment om fundamentets tyngdepunkt (valgfri)"
)

gamma_G = st.sidebar.number_input(
    "Lastfaktor ugunstig γG",
    min_value=1.0,
    max_value=1.5,
    value=1.35,
    step=0.05,
    help="Partialkoeffisient for permanente laster (EC0)"
)

# --- BEREGNINGER ---

# Dimensjonerende parametere
phi_d_rad = np.arctan(np.tan(np.radians(phi_k)) / gamma_phi)
phi_d = np.degrees(phi_d_rad)
c_d = c_k / gamma_c

# Dimensjonerende laster
V_d = gamma_G * V_k
H_d = gamma_G * H_k
M_d = gamma_G * M_k

# Effektiv bredde (reduksjon pga ekssentrisitet)
e_B = M_d / V_d if V_d > 0 else 0
B_eff = B - 2 * abs(e_B)
B_eff = max(B_eff, 0.1)  # Sikkerhet

# Effektiv lengde
e_L = 0  # Forenkling: antar moment kun i B-retning
L_eff = L - 2 * abs(e_L)

# Arealfaktor
A_eff = B_eff * L_eff

# Bæreevnefaktorer (Brinch Hansen / EC7)
N_q = np.exp(np.pi * np.tan(phi_d_rad)) * np.tan(np.radians(45 + phi_d / 2))**2
N_c = (N_q - 1) / np.tan(phi_d_rad) if phi_d > 0.1 else 5.14  # Prandtl for phi=0
N_gamma = 2 * (N_q - 1) * np.tan(phi_d_rad)

# Formfaktorer (Brinch Hansen)
s_q = 1 + (B_eff / L_eff) * np.sin(phi_d_rad)
s_c = (s_q * N_q - 1) / (N_q - 1) if N_q > 1 else 1
s_gamma = 1 - 0.3 * (B_eff / L_eff)

# Dybdefaktorer (Brinch Hansen, forenklet)
d_q = 1 + 2 * np.tan(phi_d_rad) * (1 - np.sin(phi_d_rad))**2 * (D / B_eff)
d_c = d_q - (1 - d_q) / (N_c * np.tan(phi_d_rad)) if N_c > 0 and phi_d > 0.1 else 1
d_gamma = 1.0  # Forenklet

# Helningstfaktorer (påvirkning av horisontallast)
if H_d > 0 and V_d > 0:
    m_B = (2 + B_eff / L_eff) / (1 + B_eff / L_eff)
    i_q = (1 - H_d / (V_d + A_eff * c_d / np.tan(phi_d_rad)))**m_B if phi_d > 0.1 else 0
    i_c = i_q - (1 - i_q) / (N_c * np.tan(phi_d_rad)) if N_c > 0 and phi_d > 0.1 else 0
    i_gamma = (1 - H_d / (V_d + A_eff * c_d / np.tan(phi_d_rad)))**(m_B + 1) if phi_d > 0.1 else 0
else:
    i_q = i_c = i_gamma = 1.0

# Effektiv overdekning
q_0 = gamma * D

# Dimensjonerende bæreevne (generell formel)
sigma_d = (
    c_d * N_c * s_c * d_c * i_c +
    q_0 * N_q * s_q * d_q * i_q +
    0.5 * gamma * B_eff * N_gamma * s_gamma * d_gamma * i_gamma
)

# Faktisk grunntrykk
q_actual = V_d / A_eff if A_eff > 0 else 0

# Utnyttelsesgrad
utnyttelse = (q_actual / sigma_d * 100) if sigma_d > 0 else 0

# Sikkerhetsfaktor
SF = sigma_d / q_actual if q_actual > 0 else float('inf')

# --- HOVEDPANEL ---

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Faktisk grunntrykk",
        value=f"{q_actual:.1f} kN/m²",
        help="q = Vd / Aeff"
    )
    
with col2:
    st.metric(
        label="Dimensjonerende bæreevne",
        value=f"{sigma_d:.1f} kN/m²",
        help="Beregnet bæreevne inkl. alle faktorer"
    )

with col3:
    utnyttelse_farge = "🟢" if utnyttelse < 80 else "🟡" if utnyttelse < 100 else "🔴"
    st.metric(
        label=f"{utnyttelse_farge} Utnyttelse",
        value=f"{utnyttelse:.1f} %",
        delta=f"SF = {SF:.2f}" if SF < 10 else "SF > 10",
        delta_color="inverse"
    )

st.divider()

# Visualisering
col_viz, col_data = st.columns([3, 2])

with col_viz:
    st.subheader("Fundamentskisse")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Terreng
    terrain_y = 0
    ax.axhline(y=terrain_y, color='brown', linewidth=2, linestyle='-', label='Terreng')
    ax.fill_between([-B*0.8, B*2], terrain_y, terrain_y + 0.3, color='tan', alpha=0.3)
    
    # Fundament
    fund_bottom = terrain_y - D
    fund_rect = Rectangle(
        (-B/2, fund_bottom),
        B, D * 0.2,
        linewidth=2,
        edgecolor='black',
        facecolor='gray',
        label='Fundament'
    )
    ax.add_patch(fund_rect)
    
    # Last (pil)
    arrow_start_y = terrain_y + 1.5
    arrow_length = 1.2
    
    if V_d > 0:
        ax.arrow(
            0, arrow_start_y, 0, -arrow_length,
            head_width=B*0.15,
            head_length=0.3,
            fc='red',
            ec='darkred',
            linewidth=2,
            label=f'Last V={V_d:.0f} kN'
        )
    
    # Horisontallast
    if H_d > 0:
        ax.arrow(
            -B*0.6, fund_bottom + D*0.1, B*0.3, 0,
            head_width=0.15,
            head_length=0.1,
            fc='blue',
            ec='darkblue',
            linewidth=1.5,
            label=f'H={H_d:.0f} kN'
        )
    
    # Dimensjoner
    ax.plot([-B/2, B/2], [fund_bottom - 0.3, fund_bottom - 0.3], 'k-', linewidth=1)
    ax.plot([-B/2, -B/2], [fund_bottom - 0.25, fund_bottom - 0.35], 'k-', linewidth=1)
    ax.plot([B/2, B/2], [fund_bottom - 0.25, fund_bottom - 0.35], 'k-', linewidth=1)
    ax.text(0, fund_bottom - 0.5, f'B = {B} m', ha='center', fontsize=10, weight='bold')
    
    ax.plot([-B/2 - 0.3, -B/2 - 0.3], [terrain_y, fund_bottom], 'k-', linewidth=1)
    ax.plot([-B/2 - 0.25, -B/2 - 0.35], [terrain_y, terrain_y], 'k-', linewidth=1)
    ax.plot([-B/2 - 0.25, -B/2 - 0.35], [fund_bottom, fund_bottom], 'k-', linewidth=1)
    ax.text(-B/2 - 0.6, (terrain_y + fund_bottom)/2, f'D = {D} m', 
            ha='center', rotation=90, fontsize=10, weight='bold')
    
    # Trykksone under fundament
    pressure_depth = B * 0.5
    pressure_width = B * 1.2
    pressure_points = np.array([
        [-B/2, fund_bottom],
        [B/2, fund_bottom],
        [pressure_width/2, fund_bottom - pressure_depth],
        [-pressure_width/2, fund_bottom - pressure_depth]
    ])
    pressure_poly = plt.Polygon(
        pressure_points,
        alpha=0.15,
        facecolor='red',
        edgecolor='red',
        linestyle='--',
        linewidth=1
    )
    ax.add_patch(pressure_poly)
    
    # Tekst
    status_text = "✓ OK" if utnyttelse < 100 else "✗ IKKE OK"
    status_color = 'green' if utnyttelse < 100 else 'red'
    
    ax.text(
        B*0.8, arrow_start_y - 0.2,
        f'Utnyttelse: {utnyttelse:.1f}%\n{status_text}',
        fontsize=12,
        weight='bold',
        color=status_color,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
    )
    
    # Akser
    ax.set_xlim(-B*0.9, B*1.5)
    ax.set_ylim(fund_bottom - pressure_depth - 0.5, arrow_start_y + 0.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Horisontal posisjon (m)', fontsize=10)
    ax.set_ylabel('Vertikal posisjon (m)', fontsize=10)
    ax.legend(loc='upper right', fontsize=9)
    
    st.pyplot(fig)
    plt.close()

with col_data:
    st.subheader("Detaljerte resultater")
    
    # Dimensjonerende parametere
    with st.expander("🔧 Dimensjonerende parametere", expanded=True):
        st.write(f"**φ'd** = {phi_d:.2f}° (karakteristisk: {phi_k:.2f}°)")
        st.write(f"**c'd** = {c_d:.2f} kN/m² (karakteristisk: {c_k:.2f} kN/m²)")
        st.write(f"**Vd** = {V_d:.1f} kN")
        if H_d > 0:
            st.write(f"**Hd** = {H_d:.1f} kN")
        if M_d > 0:
            st.write(f"**Md** = {M_d:.1f} kNm")
    
    # Bæreevnefaktorer
    with st.expander("📐 Bæreevnefaktorer"):
        st.write(f"**Nc** = {N_c:.2f}")
        st.write(f"**Nq** = {N_q:.2f}")
        st.write(f"**Nγ** = {N_gamma:.2f}")
        st.write("---")
        st.write(f"**sq** = {s_q:.3f} (formfaktor)")
        st.write(f"**dq** = {d_q:.3f} (dybdefaktor)")
        if H_d > 0:
            st.write(f"**iq** = {i_q:.3f} (helningstfaktor)")
    
    # Effektive dimensjoner
    with st.expander("📏 Effektive dimensjoner"):
        st.write(f"**Ekssentrisitet eB** = {e_B:.3f} m")
        st.write(f"**Effektiv bredde B'** = {B_eff:.2f} m")
        st.write(f"**Effektivt areal A'** = {A_eff:.2f} m²")
    
    # Bruddgrenser
    with st.expander("⚠️ Sikkerhetsvurdering"):
        if utnyttelse < 80:
            st.success("✓ God margin til brudd")
        elif utnyttelse < 100:
            st.warning("⚠ Moderat utnyttelse - vurder økt sikkerhet")
        else:
            st.error("✗ Utilstrekkelig bæreevne!")
        
        st.write(f"**Sikkerhetsfaktor:** {SF:.2f}")
        st.write(f"**Restkapasitet:** {sigma_d - q_actual:.1f} kN/m²")

# Resultattabell
st.divider()
st.subheader("📊 Oppsummering")

results_df = pd.DataFrame({
    'Parameter': [
        'Karakteristisk last Vk',
        'Dimensjonerende last Vd',
        'Fundamentbredde B',
        'Fundamentdybde D',
        'Effektiv bredde B\'',
        'Effektivt areal A\'',
        'Faktisk grunntrykk q',
        'Dimensjonerende bæreevne σd',
        'Utnyttelsesgrad',
        'Sikkerhetsfaktor SF'
    ],
    'Verdi': [
        f'{V_k:.1f} kN',
        f'{V_d:.1f} kN',
        f'{B:.2f} m',
        f'{D:.2f} m',
        f'{B_eff:.2f} m',
        f'{A_eff:.2f} m²',
        f'{q_actual:.1f} kN/m²',
        f'{sigma_d:.1f} kN/m²',
        f'{utnyttelse:.1f} %',
        f'{SF:.2f}'
    ]
})

st.dataframe(results_df, use_container_width=True, hide_index=True)

# Nedlastingsknapp for rapport
st.divider()

rapport = f"""
GEOTEKNISK BÆREEVNEANALYSE
===========================

INNDATA
-------
Grunnforhold:
  - Friksjonsvinkel φ'k: {phi_k}°
  - Attraksjon c'k: {c_k} kN/m²
  - Romvekt γ: {gamma} kN/m³

Fundamentgeometri:
  - Bredde B: {B} m
  - Lengde L: {L} m
  - Dybde D: {D} m

Laster:
  - Vertikallast Vk: {V_k} kN
  - Horisontallast Hk: {H_k} kN
  - Moment Mk: {M_k} kNm

BEREGNING
---------
Dimensjonerende parametere:
  - φ'd = {phi_d:.2f}°
  - c'd = {c_d:.2f} kN/m²
  - Vd = {V_d:.1f} kN

Bæreevnefaktorer:
  - Nc = {N_c:.2f}
  - Nq = {N_q:.2f}
  - Nγ = {N_gamma:.2f}

Effektive dimensjoner:
  - Ekssentrisitet: {e_B:.3f} m
  - Effektiv bredde: {B_eff:.2f} m
  - Effektivt areal: {A_eff:.2f} m²

RESULTAT
--------
Faktisk grunntrykk: {q_actual:.1f} kN/m²
Dimensjonerende bæreevne: {sigma_d:.1f} kN/m²
Utnyttelsesgrad: {utnyttelse:.1f} %
Sikkerhetsfaktor: {SF:.2f}

KONKLUSJON
----------
{'✓ Bæreevnen er tilfredsstillende' if utnyttelse < 100 else '✗ Utilstrekkelig bæreevne - fundamentet må redesignes'}

Beregnet i henhold til Eurocode 7 (NS-EN 1997-1)
Dato: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
"""

st.download_button(
    label="📄 Last ned rapport (TXT)",
    data=rapport,
    file_name=f"baereevneanalyse_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.txt",
    mime="text/plain"
)

# Footer
st.divider()
st.caption("⚠️ Dette er et forenklET beregningsverktøy. For endelige dimensjoneringer skal fullstendig geoteknisk analyse utføres av kvalifisert fagperson.")
st.caption("📚 Basert på NS-EN 1997-1 (Eurocode 7) og Brinch Hansen's metode")
