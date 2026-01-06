"""
Dashboard QoS Telekomunikasi - ULTIMATE REDESIGN
✅ Separated 2G & 4G Dashboards
✅ Enhanced Interactive UI/UX
✅ Technology Mode Selector
✅ Comparison Mode
✅ Animated Metrics & Charts
✅ Download Capabilities
✅ Advanced Filters
✅ Production Ready
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import glob
from datetime import datetime
import warnings
import base64
from io import BytesIO
warnings.filterwarnings('ignore')

# ===== CONFIGURATION =====
st.set_page_config(
    page_title="QoS Dashboard - 2G & 4G",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== ENHANCED STYLING =====
st.markdown("""
    <style>
    /* Main Header with Animation */
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        background: linear-gradient(120deg, #1f77b4, #2ecc71, #f39c12, #e74c3c);
        background-size: 300% 300%;
        animation: gradient 5s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    
    /* Technology Mode Cards */
    .tech-mode-2g {
        background: linear-gradient(135deg, #95a5a6, #7f8c8d);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .tech-mode-2g:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .tech-mode-4g {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .tech-mode-4g:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .tech-mode-comparison {
        background: linear-gradient(135deg, #9b59b6, #8e44ad);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .tech-mode-comparison:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Metric Cards with Animation */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-left: 5px solid #3498db;
        margin: 0.5rem 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card-2g {
        border-left-color: #95a5a6;
    }
    
    .metric-card-4g {
        border-left-color: #3498db;
    }
    
    /* Quality Badges */
    .quality-excellent {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        margin: 0.2rem;
        box-shadow: 0 2px 10px rgba(46, 204, 113, 0.3);
    }
    
    .quality-good {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        margin: 0.2rem;
        box-shadow: 0 2px 10px rgba(52, 152, 219, 0.3);
    }
    
    .quality-fair {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        margin: 0.2rem;
        box-shadow: 0 2px 10px rgba(243, 156, 18, 0.3);
    }
    
    .quality-poor {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        margin: 0.2rem;
        box-shadow: 0 2px 10px rgba(231, 76, 60, 0.3);
    }
    
    /* Info Cards */
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        padding: 1rem 0;
        border-bottom: 3px solid #3498db;
        margin: 1.5rem 0 1rem 0;
    }
    
    .section-header-2g {
        border-bottom-color: #95a5a6;
    }
    
    .section-header-4g {
        border-bottom-color: #3498db;
    }
    
    /* Download Button */
    .download-btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        text-align: center;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .download-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Operator Badge */
    .operator-indosat {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #000;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .operator-telkomsel {
        background: linear-gradient(135deg, #DC143C, #8B0000);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .operator-xl {
        background: linear-gradient(135deg, #4169E1, #0000CD);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    /* Animated Loading */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* Separator */
    .separator {
        border-top: 2px dashed #bdc3c7;
        margin: 2rem 0;
    }
    
    /* Best Badge */
    .best-badge {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #000;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Conclusion Card */
    .conclusion-card {
        background-color: #ffffff;
        border-left: 5px solid #3498db;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .conclusion-card:hover {
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        transform: translateX(5px);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        .tech-mode-2g, .tech-mode-4g, .tech-mode-comparison {
            font-size: 1rem;
            padding: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ===== CONSTANTS =====
ALLOWED_OPERATORS = ['Indosat', 'Telkomsel', 'XL']
OPERATOR_COLORS = {'Indosat': '#FFD700', 'Telkomsel': '#DC143C', 'XL': '#4169E1'}
DATA_FOLDER = 'data'

# ===== FILE MANAGEMENT =====
def get_data_files(folder='data'):
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except:
            pass
        return []
    files = []
    for ext in ['*.xlsx', '*.xls', '*.csv']:
        files.extend(glob.glob(os.path.join(folder, ext)))
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files

def get_file_info(filepath):
    try:
        stat = os.stat(filepath)
        return {
            'name': os.path.basename(filepath),
            'size': f"{stat.st_size / (1024 * 1024):.2f} MB",
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }
    except:
        return None

# ===== DATA LOADING =====
def identify_numeric_columns(df):
    keywords = ['Average', 'Median', 'Max', 'Min', 'Success', 'SR', '(%)', 
                'Speed', 'Mbps', 'RSRP', 'RSRQ', 'SINR', 'Latency', 'RTT',
                'YouTube', 'Youtube', 'Quality', 'MOS', 'CST', 'Sample',
                'TTFP', 'Visual', 'Freezing', 'Jerkiness', 'Browsing', 'Ping',
                'Packet', 'Loss', 'Lat', 'Long', 'RxLev', 'RxQual', '2G']
    skip = ['No.', 'Zona', 'Kabupaten / Kota', 'Lokasi Pengukuran',
            'Tanggal Pengukuran', 'Operator', 'Category', 'Jenis Tes']
    numeric_cols = []
    for col in df.columns:
        if str(col) in skip:
            continue
        for kw in keywords:
            if kw in str(col):
                numeric_cols.append(col)
                break
    return numeric_cols

def convert_to_numeric_safe(df, columns):
    df_copy = df.copy()
    for col in columns:
        if col in df_copy.columns:
            try:
                df_copy[col] = df_copy[col].replace({
                    'No Data': np.nan, 'no data': np.nan,
                    'N/A': np.nan, 'n/a': np.nan,
                    '-': np.nan, '': np.nan, ' ': np.nan
                })
                df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')
            except:
                df_copy[col] = np.nan
    return df_copy

@st.cache_data(show_spinner=False)
def load_and_prepare_data(file_path):
    try:
        if isinstance(file_path, str):
            file_ext = file_path.split('.')[-1].lower()
        else:
            file_ext = file_path.name.split('.')[-1].lower()
        
        if file_ext == 'xlsx':
            try:
                df = pd.read_excel(file_path, sheet_name='Compile_Summary', engine='openpyxl')
            except:
                df = pd.read_excel(file_path, sheet_name=0, engine='openpyxl')
        elif file_ext == 'xls':
            try:
                df = pd.read_excel(file_path, sheet_name='Compile_Summary', engine='xlrd')
            except:
                df = pd.read_excel(file_path, sheet_name=0, engine='xlrd')
        elif file_ext == 'csv':
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        else:
            return None, f"Format tidak didukung: {file_ext}"
        
        required = ['Operator', 'Kabupaten / Kota', 'Lokasi Pengukuran']
        missing = [c for c in required if c not in df.columns]
        if missing:
            return None, f"Kolom tidak ada: {', '.join(missing)}"
        
        df = df[df['Operator'].isin(ALLOWED_OPERATORS)].copy()
        if len(df) == 0:
            return None, "Tidak ada data untuk Indosat, Telkomsel, XL"
        
        df = df.dropna(subset=['Operator', 'Kabupaten / Kota'])
        
        if 'Tanggal Pengukuran' in df.columns:
            df['Tanggal Pengukuran'] = pd.to_datetime(df['Tanggal Pengukuran'], errors='coerce')
            df['Tanggal_Only'] = df['Tanggal Pengukuran'].dt.date
        
        numeric_cols = identify_numeric_columns(df)
        df = convert_to_numeric_safe(df, numeric_cols)
        
        if 'Lat' in df.columns:
            df['Lat'] = pd.to_numeric(df['Lat'], errors='coerce')
        if 'Long' in df.columns:
            df['Long'] = pd.to_numeric(df['Long'], errors='coerce')
        
        return df, None
    except Exception as e:
        return None, f"Error: {str(e)}"

# ===== HELPER FUNCTIONS =====
def safe_agg(series, func='mean'):
    try:
        if func == 'mean':
            return series.mean() if series.notna().any() else np.nan
        elif func == 'min':
            return series.min() if series.notna().any() else np.nan
        elif func == 'max':
            return series.max() if series.notna().any() else np.nan
        else:
            return np.nan
    except:
        return np.nan

def create_enhanced_chart(data, x_col, y_col, title, color_col='Operator', chart_type='signal'):
    """Enhanced chart with animations and better styling"""
    try:
        if y_col not in data.columns:
            return None
        plot_data = data[[x_col, y_col, color_col]].dropna(subset=[y_col])
        if plot_data.empty:
            return None
        
        fig = px.bar(plot_data, x=x_col, y=y_col, color=color_col, barmode='group',
                    title=title, color_discrete_map=OPERATOR_COLORS, text=y_col)
        
        if chart_type == 'signal':
            y_min = plot_data[y_col].min()
            padding = abs(y_min) * 0.1
            y_range = [y_min - padding, 5]
        else:
            y_max = plot_data[y_col].max()
            y_range = [0, y_max * 1.15]
        
        fig.update_layout(
            height=500,
            hovermode='x unified',
            xaxis={'tickangle': -45, 'title': None, 'showgrid': False},
            yaxis={'title': y_col.split('(')[0].strip(), 'range': y_range,
                   'zeroline': True, 'zerolinewidth': 3, 'zerolinecolor': '#000',
                   'showgrid': True, 'gridwidth': 1, 'gridcolor': '#ecf0f1'},
            legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02,
                   'xanchor': 'center', 'x': 0.5, 'title': None},
            title={'text': title, 'x': 0.5, 'xanchor': 'center', 'font': {'size': 18, 'color': '#2c3e50'}},
            margin={'t': 80, 'b': 100, 'l': 80, 'r': 40},
            plot_bgcolor='white',
            paper_bgcolor='#f8f9fa',
            font={'family': 'Arial, sans-serif'}
        )
        
        fig.update_traces(
            texttemplate='%{text:.1f}',
            textposition='outside',
            textfont={'size': 10, 'color': '#2c3e50'},
            marker={'line': {'width': 1, 'color': '#2c3e50'}}
        )
        
        if chart_type == 'signal':
            fig.add_hline(y=0, line_dash="solid", line_color="#34495e", line_width=2,
                         annotation_text="Baseline", annotation_position="right")
        
        return fig
    except:
        return None

def create_interactive_map(data, tech_mode='4G'):
    """Enhanced interactive map with tech-specific styling"""
    try:
        map_data = data[data['Lat'].notna() & data['Long'].notna()].copy()
        
        if map_data.empty:
            return None
        
        hover_texts = []
        for _, row in map_data.iterrows():
            text = f"<b>{row['Lokasi Pengukuran']}</b><br>"
            text += f"<b>Operator:</b> {row['Operator']}<br>"
            text += "━━━━━━━━━━━━━━━━━━━<br>"
            
            if tech_mode in ['2G', 'COMPARISON']:
                if 'Average RxLev (2G)' in row and pd.notna(row['Average RxLev (2G)']):
                    text += f"<b>📶 2G</b><br>"
                    text += f"RxLev: {row['Average RxLev (2G)']:.1f} dBm<br>"
                if 'Average RxQual (2G)' in row and pd.notna(row['Average RxQual (2G)']):
                    text += f"RxQual: {row['Average RxQual (2G)']:.1f}<br>"
                if tech_mode == 'COMPARISON':
                    text += "<br>"
            
            if tech_mode in ['4G', 'COMPARISON']:
                if 'Average RSRP (Signal Strenght 4G)' in row and pd.notna(row['Average RSRP (Signal Strenght 4G)']):
                    text += f"<b>📡 4G</b><br>"
                    text += f"RSRP: {row['Average RSRP (Signal Strenght 4G)']:.1f} dBm<br>"
                if 'Average Speed Test DL (Mbps) (4G)' in row and pd.notna(row['Average Speed Test DL (Mbps) (4G)']):
                    text += f"DL: {row['Average Speed Test DL (Mbps) (4G)']:.1f} Mbps<br>"
                if 'Youtube SR (%)' in row and pd.notna(row['Youtube SR (%)']):
                    text += f"YouTube: {row['Youtube SR (%)']:.1f}%<br>"
            
            if 'Tanggal_Only' in row and pd.notna(row['Tanggal_Only']):
                text += f"<br>📅 {row['Tanggal_Only']}"
            
            hover_texts.append(text)
        
        map_data['hover_text'] = hover_texts
        
        fig = px.scatter_mapbox(
            map_data,
            lat='Lat',
            lon='Long',
            color='Operator',
            color_discrete_map=OPERATOR_COLORS,
            hover_name='Lokasi Pengukuran',
            hover_data={'Lat': False, 'Long': False, 'Operator': True, 'hover_text': False},
            zoom=9,
            height=700,
            title=f"🗺️ Peta Lokasi Pengukuran - {tech_mode}"
        )
        
        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox=dict(
                center=dict(lat=map_data['Lat'].mean(), lon=map_data['Long'].mean()),
                zoom=9
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=0.02,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(255,255,255,0.9)"
            ),
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            title={'font': {'size': 20, 'color': '#2c3e50'}}
        )
        
        fig.update_traces(marker=dict(size=14, opacity=0.8), hovertemplate='%{hovertext}<extra></extra>')
        
        for i, trace in enumerate(fig.data):
            op = trace.name
            op_data = map_data[map_data['Operator'] == op]
            trace.hovertemplate = op_data['hover_text'].values
        
        return fig
    except Exception as e:
        st.error(f"Error creating map: {str(e)}")
        return None

def categorize_quality(value, metric_type):
    if pd.isna(value):
        return "No Data", "quality-poor"
    if metric_type == 'rsrp':
        if value >= -80: return "Excellent", "quality-excellent"
        elif value >= -90: return "Good", "quality-good"
        elif value >= -100: return "Fair", "quality-fair"
        else: return "Poor", "quality-poor"
    elif metric_type == 'rxlev':
        if value >= -75: return "Excellent", "quality-excellent"
        elif value >= -85: return "Good", "quality-good"
        elif value >= -95: return "Fair", "quality-fair"
        else: return "Poor", "quality-poor"
    elif metric_type == 'rxqual':
        if value <= 2: return "Excellent", "quality-excellent"
        elif value <= 4: return "Good", "quality-good"
        elif value <= 5: return "Fair", "quality-fair"
        else: return "Poor", "quality-poor"
    elif metric_type == 'speed':
        if value >= 30: return "Excellent", "quality-excellent"
        elif value >= 15: return "Good", "quality-good"
        elif value >= 5: return "Fair", "quality-fair"
        else: return "Poor", "quality-poor"
    elif metric_type == 'percentage':
        if value >= 95: return "Excellent", "quality-excellent"
        elif value >= 85: return "Good", "quality-good"
        elif value >= 70: return "Fair", "quality-fair"
        else: return "Poor", "quality-poor"
    return "Unknown", "quality-poor"

def create_metric_card(label, value, delta=None, tech='4G'):
    """Create animated metric card"""
    card_class = f"metric-card metric-card-{tech.lower()}"
    delta_html = ""
    if delta is not None:
        color = "green" if delta > 0 else "red" if delta < 0 else "gray"
        arrow = "▲" if delta > 0 else "▼" if delta < 0 else "━"
        delta_html = f"<div style='color: {color}; font-size: 0.9rem;'>{arrow} {delta:+.1f}%</div>"
    
    return f"""
    <div class='{card_class}'>
        <div style='font-size: 0.9rem; color: #7f8c8d; font-weight: 600;'>{label}</div>
        <div style='font-size: 2rem; color: #2c3e50; font-weight: bold; margin: 0.5rem 0;'>{value}</div>
        {delta_html}
    </div>
    """

def download_dataframe_as_excel(df, filename):
    """Create download link for Excel file"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" class="download-btn">📥 Download {filename}</a>'
    return href

# ===== DASHBOARD SECTIONS =====
def render_2g_dashboard(df_filtered):
    """Complete 2G Dashboard"""
    st.markdown('<div class="tech-mode-2g">📶 2G Technology Dashboard</div>', unsafe_allow_html=True)
    
    # Check 2G data availability
    has_2g = ('Average RxLev (2G)' in df_filtered.columns or 'Average RxQual (2G)' in df_filtered.columns)
    
    if not has_2g:
        st.warning("⚠️ Data 2G tidak tersedia dalam dataset")
        return
    
    # Overview Metrics
    st.markdown('<div class="section-header section-header-2g">📊 2G Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'Average RxLev (2G)' in df_filtered.columns:
            avg_rxlev = df_filtered['Average RxLev (2G)'].mean()
            st.markdown(create_metric_card("Avg RxLev", f"{avg_rxlev:.1f} dBm", tech='2G'), unsafe_allow_html=True)
    
    with col2:
        if 'Average RxQual (2G)' in df_filtered.columns:
            avg_rxqual = df_filtered['Average RxQual (2G)'].mean()
            st.markdown(create_metric_card("Avg RxQual", f"{avg_rxqual:.1f}", tech='2G'), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card("Locations", str(df_filtered['Lokasi Pengukuran'].nunique()), tech='2G'), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card("Operators", str(df_filtered['Operator'].nunique()), tech='2G'), unsafe_allow_html=True)
    
    # Charts
    st.markdown('<div class="section-header section-header-2g">📈 2G Signal Quality</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📶 RxLev", "📶 RxQual"])
    
    with tab1:
        if 'Average RxLev (2G)' in df_filtered.columns:
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Average RxLev (2G)': lambda x: safe_agg(x)
            })
            fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                'Average RxLev (2G)', '2G RxLev - Received Signal Level', chart_type='signal')
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                st.caption("📌 **Thresholds:** Excellent: ≥-75 dBm | Good: -75 to -85 | Fair: -85 to -95 | Poor: <-95")
    
    with tab2:
        if 'Average RxQual (2G)' in df_filtered.columns:
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Average RxQual (2G)': lambda x: safe_agg(x)
            })
            fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                'Average RxQual (2G)', '2G RxQual - Signal Quality Index', chart_type='speed')
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                st.caption("📌 **Thresholds:** Excellent: ≤2 | Good: 3-4 | Fair: 5 | Poor: ≥6 (Lower is Better)")
    
    # Data Table
    st.markdown('<div class="section-header section-header-2g">📋 2G Data Summary</div>', unsafe_allow_html=True)
    
    cols_2g = ['Operator', 'Lokasi Pengukuran', 'Average RxLev (2G)', 'Average RxQual (2G)']
    display_cols = [c for c in cols_2g if c in df_filtered.columns]
    
    if display_cols:
        st.dataframe(
            df_filtered[display_cols].sort_values('Lokasi Pengukuran'),
            use_container_width=True,
            height=400
        )
        
        # Download Button
        st.markdown(download_dataframe_as_excel(df_filtered[display_cols], "2G_Data.xlsx"), unsafe_allow_html=True)

def render_4g_dashboard(df_filtered):
    """Complete 4G Dashboard"""
    st.markdown('<div class="tech-mode-4g">📡 4G Technology Dashboard</div>', unsafe_allow_html=True)
    
    # Overview Metrics
    st.markdown('<div class="section-header section-header-4g">📊 4G Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'Average RSRP (Signal Strenght 4G)' in df_filtered.columns:
            avg_rsrp = df_filtered['Average RSRP (Signal Strenght 4G)'].mean()
            st.markdown(create_metric_card("Avg RSRP", f"{avg_rsrp:.1f} dBm", tech='4G'), unsafe_allow_html=True)
    
    with col2:
        if 'Average Speed Test DL (Mbps) (4G)' in df_filtered.columns:
            avg_dl = df_filtered['Average Speed Test DL (Mbps) (4G)'].mean()
            st.markdown(create_metric_card("Avg DL Speed", f"{avg_dl:.1f} Mbps", tech='4G'), unsafe_allow_html=True)
    
    with col3:
        if 'Youtube SR (%)' in df_filtered.columns:
            avg_yt = df_filtered['Youtube SR (%)'].mean()
            st.markdown(create_metric_card("YouTube SR", f"{avg_yt:.1f}%", tech='4G'), unsafe_allow_html=True)
    
    with col4:
        if 'Average RTT Latency (ms)' in df_filtered.columns:
            avg_lat = df_filtered['Average RTT Latency (ms)'].mean()
            st.markdown(create_metric_card("Avg Latency", f"{avg_lat:.1f} ms", tech='4G'), unsafe_allow_html=True)
    
    # Charts Tabs
    st.markdown('<div class="section-header section-header-4g">📈 4G Performance</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📡 Signal", "🚀 Speed", "🌐 Browsing", "🏓 Ping", "📹 YouTube"])
    
    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            if 'Average RSRP (Signal Strenght 4G)' in df_filtered.columns:
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average RSRP (Signal Strenght 4G)': lambda x: safe_agg(x)
                })
                fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                    'Average RSRP (Signal Strenght 4G)', '4G RSRP', chart_type='signal')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        with col_b:
            if 'Average RSRQ (Signal Qualty 4G)' in df_filtered.columns:
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average RSRQ (Signal Qualty 4G)': lambda x: safe_agg(x)
                })
                fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                    'Average RSRQ (Signal Qualty 4G)', '4G RSRQ', chart_type='signal')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col_a, col_b = st.columns(2)
        with col_a:
            if 'Average Speed Test DL (Mbps) (4G)' in df_filtered.columns:
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average Speed Test DL (Mbps) (4G)': lambda x: safe_agg(x)
                })
                fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                    'Average Speed Test DL (Mbps) (4G)', 'Download Speed', chart_type='speed')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        with col_b:
            if 'Average Speed Test UL (Mbps) (4G)' in df_filtered.columns:
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average Speed Test UL (Mbps) (4G)': lambda x: safe_agg(x)
                })
                fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                    'Average Speed Test UL (Mbps) (4G)', 'Upload Speed', chart_type='speed')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        if 'Browsing Success (%)' in df_filtered.columns:
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Browsing Success (%)': lambda x: safe_agg(x)
            })
            fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                'Browsing Success (%)', 'Browsing Success Rate', chart_type='speed')
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        if 'Average RTT Latency (ms)' in df_filtered.columns:
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Average RTT Latency (ms)': lambda x: safe_agg(x)
            })
            fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                'Average RTT Latency (ms)', 'Ping Latency', chart_type='speed')
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        if 'Youtube SR (%)' in df_filtered.columns:
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Youtube SR (%)': lambda x: safe_agg(x)
            })
            fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                'Youtube SR (%)', 'YouTube Success Rate', chart_type='speed')
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    # Data Table
    st.markdown('<div class="section-header section-header-4g">📋 4G Data Summary</div>', unsafe_allow_html=True)
    
    cols_4g = ['Operator', 'Lokasi Pengukuran', 'Average RSRP (Signal Strenght 4G)', 
               'Average Speed Test DL (Mbps) (4G)', 'Youtube SR (%)', 'Average RTT Latency (ms)']
    display_cols = [c for c in cols_4g if c in df_filtered.columns]
    
    if display_cols:
        st.dataframe(
            df_filtered[display_cols].sort_values('Lokasi Pengukuran'),
            use_container_width=True,
            height=400
        )
        
        # Download Button
        st.markdown(download_dataframe_as_excel(df_filtered[display_cols], "4G_Data.xlsx"), unsafe_allow_html=True)

def render_comparison_dashboard(df_filtered):
    """Side-by-side comparison of 2G and 4G"""
    st.markdown('<div class="tech-mode-comparison">🔄 2G vs 4G Comparison</div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    # 2G Side
    with col_left:
        st.markdown('<div class="section-header section-header-2g">📶 2G Metrics</div>', unsafe_allow_html=True)
        
        if 'Average RxLev (2G)' in df_filtered.columns:
            avg_rxlev = df_filtered['Average RxLev (2G)'].mean()
            st.markdown(create_metric_card("Avg RxLev", f"{avg_rxlev:.1f} dBm", tech='2G'), unsafe_allow_html=True)
        
        if 'Average RxQual (2G)' in df_filtered.columns:
            avg_rxqual = df_filtered['Average RxQual (2G)'].mean()
            st.markdown(create_metric_card("Avg RxQual", f"{avg_rxqual:.1f}", tech='2G'), unsafe_allow_html=True)
    
    # 4G Side
    with col_right:
        st.markdown('<div class="section-header section-header-4g">📡 4G Metrics</div>', unsafe_allow_html=True)
        
        if 'Average RSRP (Signal Strenght 4G)' in df_filtered.columns:
            avg_rsrp = df_filtered['Average RSRP (Signal Strenght 4G)'].mean()
            st.markdown(create_metric_card("Avg RSRP", f"{avg_rsrp:.1f} dBm", tech='4G'), unsafe_allow_html=True)
        
        if 'Average Speed Test DL (Mbps) (4G)' in df_filtered.columns:
            avg_dl = df_filtered['Average Speed Test DL (Mbps) (4G)'].mean()
            st.markdown(create_metric_card("Avg DL Speed", f"{avg_dl:.1f} Mbps", tech='4G'), unsafe_allow_html=True)
    
    # Side-by-side charts
    st.markdown('<div class="section-header">📊 Performance Comparison</div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        if 'Average RxLev (2G)' in df_filtered.columns:
            st.markdown("**2G RxLev**")
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Average RxLev (2G)': lambda x: safe_agg(x)
            })
            fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                'Average RxLev (2G)', '2G RxLev', chart_type='signal')
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        if 'Average RSRP (Signal Strenght 4G)' in df_filtered.columns:
            st.markdown("**4G RSRP**")
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Average RSRP (Signal Strenght 4G)': lambda x: safe_agg(x)
            })
            fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                'Average RSRP (Signal Strenght 4G)', '4G RSRP', chart_type='signal')
            if fig:
                st.plotly_chart(fig, use_container_width=True)

# ===== MAIN APP =====
def main():
    # Header
    st.markdown('<p class="main-header">📡 QoS Dashboard - 2G & 4G Analysis</p>', unsafe_allow_html=True)
    
    # Sidebar - File Management
    with st.sidebar:
        st.title("📁 Data Source")
        
        data_files = get_data_files(DATA_FOLDER)
        file_path = None
        
        if data_files:
            st.success(f"✅ {len(data_files)} file(s) found")
            file_names = [os.path.basename(f) for f in data_files]
            selected_file = st.selectbox("📂 Select File", file_names, key='file_select')
            idx = file_names.index(selected_file)
            file_path = data_files[idx]
            info = get_file_info(file_path)
            if info:
                st.info(f"📊 Size: {info['size']}")
                st.caption(f"Modified: {info['modified']}")
        else:
            st.warning(f"⚠️ No files in '{DATA_FOLDER}' folder")
            uploaded = st.file_uploader("📤 Upload File", type=['xlsx', 'xls', 'csv'])
            if uploaded:
                file_path = uploaded
                st.success(f"✅ {uploaded.name}")
            else:
                st.info(f"Create '{DATA_FOLDER}' folder and place files there")
                return
    
    # Load Data
    with st.spinner('⏳ Loading data...'):
        df, error = load_and_prepare_data(file_path)
    
    if error:
        st.error(f"❌ {error}")
        return
    
    if df is None or len(df) == 0:
        st.error("❌ No data available")
        return
    
    # Sidebar - Technology Mode Selector
    with st.sidebar:
        st.markdown("---")
        st.title("🎯 Technology Mode")
        
        tech_mode = st.radio(
            "Select Dashboard Mode",
            ["📶 2G Dashboard", "📡 4G Dashboard", "🔄 Comparison"],
            key='tech_mode',
            help="Choose which technology dashboard to view"
        )
        
        st.markdown("---")
        st.title("🔍 Filters")
        
        # Kabupaten Filter
        kab_opts = ['All'] + sorted([str(k) for k in df['Kabupaten / Kota'].unique() if pd.notna(k)])
        sel_kab = st.selectbox("📍 Kabupaten", kab_opts, key='kab_filter')
        
        df_filtered = df.copy()
        if sel_kab != 'All':
            df_filtered = df_filtered[df_filtered['Kabupaten / Kota'] == sel_kab]
        
        # Date Filter
        has_date = 'Tanggal_Only' in df_filtered.columns and df_filtered['Tanggal_Only'].notna().any()
        
        if has_date:
            st.markdown("**📅 Date Range**")
            date_filter = st.radio("", ["All Dates", "Specific Date"], horizontal=True, key='date_filter')
            if date_filter == "Specific Date":
                dates = sorted(df_filtered['Tanggal_Only'].dropna().unique())
                sel_date = st.selectbox("", dates,
                    format_func=lambda x: pd.to_datetime(x).strftime('%d %B %Y'),
                    key='date_select')
                df_filtered = df_filtered[df_filtered['Tanggal_Only'] == sel_date]
        
        # Location Filter
        lok_opts = ['All'] + sorted([str(l) for l in df_filtered['Lokasi Pengukuran'].unique() if pd.notna(l)])
        sel_lok = st.selectbox("📍 Location", lok_opts, key='loc_filter')
        if sel_lok != 'All':
            df_filtered = df_filtered[df_filtered['Lokasi Pengukuran'] == sel_lok]
        
        # Operator Filter
        op_opts = ['All'] + sorted(ALLOWED_OPERATORS)
        sel_ops = st.multiselect("👥 Operators", op_opts, default='All', key='op_filter')
        if 'All' not in sel_ops and sel_ops:
            df_filtered = df_filtered[df_filtered['Operator'].isin(sel_ops)]
        
        st.markdown("---")
        
        # Summary Stats
        col1, col2 = st.columns(2)
        col1.metric("📊 Records", f"{len(df_filtered):,}")
        col2.metric("📍 Locations", df_filtered['Lokasi Pengukuran'].nunique())
    
    if df_filtered.empty:
        st.warning("⚠️ No data matches the selected filters")
        return
    
    # Render Dashboard based on Mode
    if tech_mode == "📶 2G Dashboard":
        render_2g_dashboard(df_filtered)
    elif tech_mode == "📡 4G Dashboard":
        render_4g_dashboard(df_filtered)
    else:  # Comparison Mode
        render_comparison_dashboard(df_filtered)
    
    # Interactive Map (Always show)
    st.markdown("---")
    st.markdown('<div class="section-header">🗺️ Interactive Location Map</div>', unsafe_allow_html=True)
    
    has_coords = 'Lat' in df_filtered.columns and 'Long' in df_filtered.columns
    valid_coords = df_filtered['Lat'].notna().sum() if has_coords else 0
    
    if has_coords and valid_coords > 0:
        map_tech = '2G' if tech_mode == "📶 2G Dashboard" else '4G' if tech_mode == "📡 4G Dashboard" else 'COMPARISON'
        fig_map = create_interactive_map(df_filtered, map_tech)
        if fig_map:
            st.plotly_chart(fig_map, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("📍 Markers", valid_coords)
            col2.metric("🌍 Lat Range", f"{(df_filtered['Lat'].max() - df_filtered['Lat'].min()):.4f}°")
            col3.metric("🌍 Long Range", f"{(df_filtered['Long'].max() - df_filtered['Long'].min()):.4f}°")
    else:
        st.info("💡 No location coordinates available for mapping")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #7f8c8d; padding: 2rem 0;'>
            <p style='font-size: 0.9rem;'>📡 QoS Dashboard | 2G & 4G Analysis Platform</p>
            <p style='font-size: 0.8rem;'>Enhanced Interactive UI/UX | Separated Technology Views</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()