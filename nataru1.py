"""
Dashboard QoS Telekomunikasi - ULTIMATE VERSION 2.0 ⭐⭐⭐
✅ Multi-Date Selection Filter (NEW!)
✅ Enhanced 2G Information (RxLev & RxQual Details) (NEW!)
✅ Dedicated Conclusion Menu per Operator (NEW!)
✅ 2G & 4G Separated Dashboards
✅ Advanced Scoring & Ranking
✅ Interactive Visualizations
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
    page_title="QoS Dashboard v2.0",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== ENHANCED STYLING =====
st.markdown("""
    <style>
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header {
        font-size: 3rem;
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
    
    .tech-mode-2g {
        background: linear-gradient(135deg, #95a5a6, #7f8c8d);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    .tech-mode-4g {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        margin: 0.5rem 0;
        border-left: 5px solid #3498db;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card-2g { border-left-color: #95a5a6; }
    .metric-card-4g { border-left-color: #3498db; }
    
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
    
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        padding: 1rem 0;
        border-bottom: 3px solid #3498db;
        margin: 1.5rem 0 1rem 0;
    }
    
    .section-header-2g { border-bottom-color: #95a5a6; }
    .section-header-4g { border-bottom-color: #3498db; }
    
    .operator-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border: 2px solid #dee2e6;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .conclusion-box {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #3498db;
    }
    
    .info-box {
        background: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .best-badge {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #000;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 3px 15px rgba(255, 215, 0, 0.4);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .download-btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.8rem 2rem;
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
    </style>
""", unsafe_allow_html=True)

# ===== CONSTANTS =====
ALLOWED_OPERATORS = ['Indosat', 'Telkomsel', 'XL']
OPERATOR_COLORS = {'Indosat': '#FFD700', 'Telkomsel': '#DC143C', 'XL': '#4169E1'}
DATA_FOLDER = 'data'

# 2G Thresholds
THRESHOLDS_2G = {
    'RxLev': {'excellent': -75, 'good': -85, 'fair': -95},
    'RxQual': {'excellent': 2, 'good': 4, 'fair': 5}
}

# 4G Thresholds
THRESHOLDS_4G = {
    'RSRP': {'excellent': -80, 'good': -90, 'fair': -100},
    'Speed': {'excellent': 30, 'good': 15, 'fair': 5},
    'Percentage': {'excellent': 95, 'good': 85, 'fair': 70}
}

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
        elif func == 'median':
            return series.median() if series.notna().any() else np.nan
        else:
            return np.nan
    except:
        return np.nan

def categorize_quality(value, metric_type):
    """Categorize signal quality based on value and type"""
    if pd.isna(value):
        return "No Data", "quality-poor"
    
    if metric_type == 'rxlev':
        if value >= THRESHOLDS_2G['RxLev']['excellent']:
            return "Excellent", "quality-excellent"
        elif value >= THRESHOLDS_2G['RxLev']['good']:
            return "Good", "quality-good"
        elif value >= THRESHOLDS_2G['RxLev']['fair']:
            return "Fair", "quality-fair"
        else:
            return "Poor", "quality-poor"
    
    elif metric_type == 'rxqual':
        if value <= THRESHOLDS_2G['RxQual']['excellent']:
            return "Excellent", "quality-excellent"
        elif value <= THRESHOLDS_2G['RxQual']['good']:
            return "Good", "quality-good"
        elif value <= THRESHOLDS_2G['RxQual']['fair']:
            return "Fair", "quality-fair"
        else:
            return "Poor", "quality-poor"
    
    elif metric_type == 'rsrp':
        if value >= THRESHOLDS_4G['RSRP']['excellent']:
            return "Excellent", "quality-excellent"
        elif value >= THRESHOLDS_4G['RSRP']['good']:
            return "Good", "quality-good"
        elif value >= THRESHOLDS_4G['RSRP']['fair']:
            return "Fair", "quality-fair"
        else:
            return "Poor", "quality-poor"
    
    elif metric_type == 'speed':
        if value >= THRESHOLDS_4G['Speed']['excellent']:
            return "Excellent", "quality-excellent"
        elif value >= THRESHOLDS_4G['Speed']['good']:
            return "Good", "quality-good"
        elif value >= THRESHOLDS_4G['Speed']['fair']:
            return "Fair", "quality-fair"
        else:
            return "Poor", "quality-poor"
    
    elif metric_type == 'percentage':
        if value >= THRESHOLDS_4G['Percentage']['excellent']:
            return "Excellent", "quality-excellent"
        elif value >= THRESHOLDS_4G['Percentage']['good']:
            return "Good", "quality-good"
        elif value >= THRESHOLDS_4G['Percentage']['fair']:
            return "Fair", "quality-fair"
        else:
            return "Poor", "quality-poor"
    
    return "Unknown", "quality-poor"

def calculate_2g_score(rxlev, rxqual):
    """Calculate 2G performance score (0-100)"""
    scores = []
    
    if pd.notna(rxlev):
        if rxlev >= -75:
            scores.append(100)
        elif rxlev >= -85:
            scores.append(75)
        elif rxlev >= -95:
            scores.append(50)
        else:
            scores.append(25)
    
    if pd.notna(rxqual):
        if rxqual <= 2:
            scores.append(100)
        elif rxqual <= 4:
            scores.append(75)
        elif rxqual <= 5:
            scores.append(50)
        else:
            scores.append(25)
    
    return np.mean(scores) if scores else 0

def calculate_4g_score(rsrp, speed_dl, browsing_sr, youtube_sr):
    """Calculate 4G performance score (0-100) with weights"""
    score = 0
    weights_used = 0
    
    # RSRP (30% weight)
    if pd.notna(rsrp):
        if rsrp >= -80:
            score += 100 * 0.3
        elif rsrp >= -90:
            score += 75 * 0.3
        elif rsrp >= -100:
            score += 50 * 0.3
        else:
            score += 25 * 0.3
        weights_used += 0.3
    
    # Download Speed (30% weight)
    if pd.notna(speed_dl):
        if speed_dl >= 30:
            score += 100 * 0.3
        elif speed_dl >= 15:
            score += 75 * 0.3
        elif speed_dl >= 5:
            score += 50 * 0.3
        else:
            score += 25 * 0.3
        weights_used += 0.3
    
    # Browsing SR (20% weight)
    if pd.notna(browsing_sr):
        if browsing_sr >= 95:
            score += 100 * 0.2
        elif browsing_sr >= 85:
            score += 75 * 0.2
        else:
            score += 50 * 0.2
        weights_used += 0.2
    
    # YouTube SR (20% weight)
    if pd.notna(youtube_sr):
        if youtube_sr >= 95:
            score += 100 * 0.2
        elif youtube_sr >= 85:
            score += 75 * 0.2
        else:
            score += 50 * 0.2
        weights_used += 0.2
    
    # Normalize if not all metrics available
    if weights_used > 0:
        score = (score / weights_used) * 1.0
    
    return score

def get_score_badge(score):
    """Get score badge class and label"""
    if score >= 85:
        return "quality-excellent", "Sangat Baik"
    elif score >= 70:
        return "quality-good", "Baik"
    elif score >= 50:
        return "quality-fair", "Cukup"
    else:
        return "quality-poor", "Perlu Perbaikan"

# ===== VISUALIZATION FUNCTIONS =====
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

def download_dataframe_as_excel(df, filename):
    """Create download link for Excel file"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" class="download-btn">📥 Download {filename}</a>'
    return href

# ===== ENHANCED 2G INFORMATION DISPLAY =====
def render_2g_detailed_info(df_operator, operator_name):
    """Render detailed 2G information with RxLev and RxQual explanations"""
    st.markdown(f"<div class='operator-card'>", unsafe_allow_html=True)
    st.markdown(f"### 👤 **{operator_name}**")
    st.markdown("")
    
    # RxLev Analysis
    if 'Average RxLev (2G)' in df_operator.columns:
        st.markdown("#### 📶 **RxLev (Received Signal Level)**")
        
        rxlev_avg = safe_agg(df_operator['Average RxLev (2G)'], 'mean')
        rxlev_min = safe_agg(df_operator['Average RxLev (2G)'], 'min')
        rxlev_max = safe_agg(df_operator['Average RxLev (2G)'], 'max')
        rxlev_median = safe_agg(df_operator['Average RxLev (2G)'], 'median')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Average", f"{rxlev_avg:.2f} dBm" if pd.notna(rxlev_avg) else "N/A")
            if pd.notna(rxlev_avg):
                cat, cls = categorize_quality(rxlev_avg, 'rxlev')
                st.markdown(f"<span class='{cls}'>{cat}</span>", unsafe_allow_html=True)
        
        with col2:
            st.metric("📈 Median", f"{rxlev_median:.2f} dBm" if pd.notna(rxlev_median) else "N/A")
        
        with col3:
            st.metric("🔺 Maximum", f"{rxlev_max:.2f} dBm" if pd.notna(rxlev_max) else "N/A")
        
        with col4:
            st.metric("🔻 Minimum", f"{rxlev_min:.2f} dBm" if pd.notna(rxlev_min) else "N/A")
        
        # RxLev Distribution
        if pd.notna(rxlev_avg):
            rxlev_data = df_operator['Average RxLev (2G)'].dropna()
            if not rxlev_data.empty:
                excellent = len(rxlev_data[rxlev_data >= -75])
                good = len(rxlev_data[(rxlev_data >= -85) & (rxlev_data < -75)])
                fair = len(rxlev_data[(rxlev_data >= -95) & (rxlev_data < -85)])
                poor = len(rxlev_data[rxlev_data < -95])
                total = len(rxlev_data)
                
                st.markdown("**📊 Signal Strength Distribution:**")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🟢 Excellent", f"{excellent} ({excellent/total*100:.1f}%)")
                col2.metric("🔵 Good", f"{good} ({good/total*100:.1f}%)")
                col3.metric("🟡 Fair", f"{fair} ({fair/total*100:.1f}%)")
                col4.metric("🔴 Poor", f"{poor} ({poor/total*100:.1f}%)")
        
        st.markdown("""
        <div class='info-box'>
        <strong>💡 RxLev Information:</strong><br>
        • <strong>What:</strong> Kekuatan sinyal yang diterima dari BTS (Base Transceiver Station)<br>
        • <strong>Unit:</strong> dBm (decibel-milliwatts)<br>
        • <strong>Range:</strong> -110 dBm (sangat lemah) to -47 dBm (sangat kuat)<br>
        • <strong>Impact:</strong> Menentukan kualitas panggilan dan kecepatan data<br>
        • <strong>Thresholds:</strong> ≥-75 (Excellent) | -75 to -85 (Good) | -85 to -95 (Fair) | <-95 (Poor)
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # RxQual Analysis
    if 'Average RxQual (2G)' in df_operator.columns:
        st.markdown("#### 📡 **RxQual (Received Signal Quality)**")
        
        rxqual_avg = safe_agg(df_operator['Average RxQual (2G)'], 'mean')
        rxqual_min = safe_agg(df_operator['Average RxQual (2G)'], 'min')
        rxqual_max = safe_agg(df_operator['Average RxQual (2G)'], 'max')
        rxqual_median = safe_agg(df_operator['Average RxQual (2G)'], 'median')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Average", f"{rxqual_avg:.2f}" if pd.notna(rxqual_avg) else "N/A")
            if pd.notna(rxqual_avg):
                cat, cls = categorize_quality(rxqual_avg, 'rxqual')
                st.markdown(f"<span class='{cls}'>{cat}</span>", unsafe_allow_html=True)
        
        with col2:
            st.metric("📈 Median", f"{rxqual_median:.2f}" if pd.notna(rxqual_median) else "N/A")
        
        with col3:
            st.metric("🔺 Maximum", f"{rxqual_max:.2f}" if pd.notna(rxqual_max) else "N/A")
        
        with col4:
            st.metric("🔻 Minimum", f"{rxqual_min:.2f}" if pd.notna(rxqual_min) else "N/A")
        
        # RxQual Distribution
        if pd.notna(rxqual_avg):
            rxqual_data = df_operator['Average RxQual (2G)'].dropna()
            if not rxqual_data.empty:
                excellent = len(rxqual_data[rxqual_data <= 2])
                good = len(rxqual_data[(rxqual_data > 2) & (rxqual_data <= 4)])
                fair = len(rxqual_data[(rxqual_data > 4) & (rxqual_data <= 5)])
                poor = len(rxqual_data[rxqual_data > 5])
                total = len(rxqual_data)
                
                st.markdown("**📊 Signal Quality Distribution:**")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🟢 Excellent", f"{excellent} ({excellent/total*100:.1f}%)")
                col2.metric("🔵 Good", f"{good} ({good/total*100:.1f}%)")
                col3.metric("🟡 Fair", f"{fair} ({fair/total*100:.1f}%)")
                col4.metric("🔴 Poor", f"{poor} ({poor/total*100:.1f}%)")
        
        st.markdown("""
        <div class='info-box'>
        <strong>💡 RxQual Information:</strong><br>
        • <strong>What:</strong> Indeks kualitas sinyal berdasarkan Bit Error Rate (BER)<br>
        • <strong>Scale:</strong> 0-7 (0 = best, 7 = worst) - <em>Lower is Better!</em><br>
        • <strong>Impact:</strong> Menentukan kejernihan suara dan stabilitas koneksi<br>
        • <strong>Thresholds:</strong> ≤2 (Excellent) | 3-4 (Good) | 5 (Fair) | ≥6 (Poor)<br>
        • <strong>Note:</strong> RxQual tinggi = banyak error, meskipun sinyal kuat
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ===== CONCLUSION GENERATORS =====
def generate_overall_conclusion_2g(df_data, operators):
    """Generate overall 2G conclusion for all operators"""
    lines = []
    lines.append("## 📊 **Kesimpulan Pengukuran 2G - Overall**")
    lines.append("")
    lines.append(f"**📅 Periode Analisis:** {df_data['Tanggal_Only'].min()} s/d {df_data['Tanggal_Only'].max()}")
    lines.append(f"**📍 Total Lokasi:** {df_data['Lokasi Pengukuran'].nunique()} lokasi")
    lines.append(f"**📊 Total Pengukuran:** {len(df_data)} records")
    lines.append("")
    lines.append("---")
    
    operator_scores = {}
    operator_details = {}
    
    for operator in operators:
        op_data = df_data[df_data['Operator'] == operator]
        
        rxlev = safe_agg(op_data['Average RxLev (2G)']) if 'Average RxLev (2G)' in op_data.columns else np.nan
        rxqual = safe_agg(op_data['Average RxQual (2G)']) if 'Average RxQual (2G)' in op_data.columns else np.nan
        
        score = calculate_2g_score(rxlev, rxqual)
        operator_scores[operator] = score
        operator_details[operator] = {'rxlev': rxlev, 'rxqual': rxqual}
        
        lines.append("")
        lines.append(f"### 👤 **{operator}**")
        lines.append("")
        
        # Signal Metrics
        if pd.notna(rxlev):
            cat, cls = categorize_quality(rxlev, 'rxlev')
            lines.append(f"**📶 RxLev (Signal Strength):** {rxlev:.2f} dBm - <span class='{cls}'>{cat}</span>")
        
        if pd.notna(rxqual):
            cat, cls = categorize_quality(rxqual, 'rxqual')
            lines.append(f"**📡 RxQual (Signal Quality):** {rxqual:.2f} - <span class='{cls}'>{cat}</span>")
        
        # Coverage Stats
        lines.append(f"**📍 Coverage:** {op_data['Lokasi Pengukuran'].nunique()} locations, {len(op_data)} measurements")
        
        # Overall Score
        badge_cls, badge_label = get_score_badge(score)
        lines.append("")
        lines.append(f"**📊 Overall Score:** <span class='{badge_cls} style='padding: 0.5rem 1rem;'>{badge_label} ({score:.0f}/100)</span>")
        lines.append("")
        lines.append("---")
    
    # Ranking
    if operator_scores:
        lines.append("")
        lines.append("## 🏆 **Ranking 2G Performance**")
        lines.append("")
        
        sorted_ops = sorted(operator_scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (op, score) in enumerate(sorted_ops, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
            badge = " <span class='best-badge'>TERBAIK 2G</span>" if rank == 1 else ""
            details = operator_details[op]
            
            lines.append(f"{medal} **{rank}. {op}**{badge}")
            lines.append(f"   - Overall Score: {score:.0f}/100")
            lines.append(f"   - RxLev: {details['rxlev']:.2f} dBm | RxQual: {details['rxqual']:.2f}")
            lines.append("")
    
    return "\n".join(lines)

def generate_overall_conclusion_4g(df_data, operators):
    """Generate overall 4G conclusion for all operators"""
    lines = []
    lines.append("## 📊 **Kesimpulan Pengukuran 4G - Overall**")
    lines.append("")
    lines.append(f"**📅 Periode Analisis:** {df_data['Tanggal_Only'].min()} s/d {df_data['Tanggal_Only'].max()}")
    lines.append(f"**📍 Total Lokasi:** {df_data['Lokasi Pengukuran'].nunique()} lokasi")
    lines.append(f"**📊 Total Pengukuran:** {len(df_data)} records")
    lines.append("")
    lines.append("---")
    
    operator_scores = {}
    operator_details = {}
    
    for operator in operators:
        op_data = df_data[df_data['Operator'] == operator]
        
        rsrp = safe_agg(op_data['Average RSRP (Signal Strenght 4G)']) if 'Average RSRP (Signal Strenght 4G)' in op_data.columns else np.nan
        speed_dl = safe_agg(op_data['Average Speed Test DL (Mbps) (4G)']) if 'Average Speed Test DL (Mbps) (4G)' in op_data.columns else np.nan
        browsing = safe_agg(op_data['Browsing Success (%)']) if 'Browsing Success (%)' in op_data.columns else np.nan
        youtube = safe_agg(op_data['Youtube SR (%)']) if 'Youtube SR (%)' in op_data.columns else np.nan
        
        score = calculate_4g_score(rsrp, speed_dl, browsing, youtube)
        operator_scores[operator] = score
        operator_details[operator] = {
            'rsrp': rsrp, 'speed': speed_dl, 
            'browsing': browsing, 'youtube': youtube
        }
        
        lines.append("")
        lines.append(f"### 👤 **{operator}**")
        lines.append("")
        
        # Metrics
        if pd.notna(rsrp):
            cat, cls = categorize_quality(rsrp, 'rsrp')
            lines.append(f"**📡 RSRP:** {rsrp:.2f} dBm - <span class='{cls}'>{cat}</span>")
        
        if pd.notna(speed_dl):
            cat, cls = categorize_quality(speed_dl, 'speed')
            lines.append(f"**🚀 Download Speed:** {speed_dl:.2f} Mbps - <span class='{cls}'>{cat}</span>")
        
        if pd.notna(browsing):
            cat, cls = categorize_quality(browsing, 'percentage')
            lines.append(f"**🌐 Browsing SR:** {browsing:.1f}% - <span class='{cls}'>{cat}</span>")
        
        if pd.notna(youtube):
            cat, cls = categorize_quality(youtube, 'percentage')
            lines.append(f"**📹 YouTube SR:** {youtube:.1f}% - <span class='{cls}'>{cat}</span>")
        
        # Coverage
        lines.append(f"**📍 Coverage:** {op_data['Lokasi Pengukuran'].nunique()} locations, {len(op_data)} measurements")
        
        # Score
        badge_cls, badge_label = get_score_badge(score)
        lines.append("")
        lines.append(f"**📊 Overall Score:** <span class='{badge_cls} style='padding: 0.5rem 1rem;'>{badge_label} ({score:.0f}/100)</span>")
        lines.append("")
        lines.append("---")
    
    # Ranking
    if operator_scores:
        lines.append("")
        lines.append("## 🏆 **Ranking 4G Performance**")
        lines.append("")
        
        sorted_ops = sorted(operator_scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (op, score) in enumerate(sorted_ops, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
            badge = " <span class='best-badge'>TERBAIK 4G</span>" if rank == 1 else ""
            details = operator_details[op]
            
            lines.append(f"{medal} **{rank}. {op}**{badge}")
            lines.append(f"   - Overall Score: {score:.0f}/100")
            lines.append(f"   - RSRP: {details['rsrp']:.2f} dBm | Speed: {details['speed']:.2f} Mbps")
            lines.append(f"   - Browsing: {details['browsing']:.1f}% | YouTube: {details['youtube']:.1f}%")
            lines.append("")
    
    return "\n".join(lines)

def generate_per_operator_conclusion_2g(df_data, operator):
    """Generate detailed 2G conclusion for specific operator"""
    lines = []
    lines.append(f"## 📊 **Kesimpulan 2G - {operator}**")
    lines.append("")
    
    op_data = df_data[df_data['Operator'] == operator]
    
    lines.append(f"**📅 Periode:** {op_data['Tanggal_Only'].min()} s/d {op_data['Tanggal_Only'].max()}")
    lines.append(f"**📍 Total Lokasi:** {op_data['Lokasi Pengukuran'].nunique()}")
    lines.append(f"**📊 Total Measurements:** {len(op_data)}")
    lines.append("")
    lines.append("---")
    
    # Overall Metrics
    lines.append("### 📈 **Overall Performance**")
    lines.append("")
    
    if 'Average RxLev (2G)' in op_data.columns:
        rxlev_avg = safe_agg(op_data['Average RxLev (2G)'], 'mean')
        rxlev_min = safe_agg(op_data['Average RxLev (2G)'], 'min')
        rxlev_max = safe_agg(op_data['Average RxLev (2G)'], 'max')
        
        if pd.notna(rxlev_avg):
            cat, cls = categorize_quality(rxlev_avg, 'rxlev')
            lines.append(f"**📶 RxLev (Signal Strength):**")
            lines.append(f"- Average: {rxlev_avg:.2f} dBm - <span class='{cls}'>{cat}</span>")
            lines.append(f"- Range: {rxlev_min:.2f} to {rxlev_max:.2f} dBm")
            lines.append("")
    
    if 'Average RxQual (2G)' in op_data.columns:
        rxqual_avg = safe_agg(op_data['Average RxQual (2G)'], 'mean')
        rxqual_min = safe_agg(op_data['Average RxQual (2G)'], 'min')
        rxqual_max = safe_agg(op_data['Average RxQual (2G)'], 'max')
        
        if pd.notna(rxqual_avg):
            cat, cls = categorize_quality(rxqual_avg, 'rxqual')
            lines.append(f"**📡 RxQual (Signal Quality):**")
            lines.append(f"- Average: {rxqual_avg:.2f} - <span class='{cls}'>{cat}</span>")
            lines.append(f"- Range: {rxqual_min:.2f} to {rxqual_max:.2f}")
            lines.append("")
    
    # Location Analysis
    lines.append("---")
    lines.append("### 📍 **Per Location Summary**")
    lines.append("")
    
    location_groups = op_data.groupby('Lokasi Pengukuran')
    for loc, loc_data in list(location_groups)[:5]:  # Top 5 locations
        rxlev_loc = safe_agg(loc_data['Average RxLev (2G)']) if 'Average RxLev (2G)' in loc_data.columns else np.nan
        rxqual_loc = safe_agg(loc_data['Average RxQual (2G)']) if 'Average RxQual (2G)' in loc_data.columns else np.nan
        
        score_loc = calculate_2g_score(rxlev_loc, rxqual_loc)
        badge_cls, badge_label = get_score_badge(score_loc)
        
        lines.append(f"**{loc}:**")
        if pd.notna(rxlev_loc):
            lines.append(f"- RxLev: {rxlev_loc:.2f} dBm")
        if pd.notna(rxqual_loc):
            lines.append(f"- RxQual: {rxqual_loc:.2f}")
        lines.append(f"- Score: <span class='{badge_cls}'>{score_loc:.0f}/100</span>")
        lines.append("")
    
    if len(location_groups) > 5:
        lines.append(f"*...dan {len(location_groups) - 5} lokasi lainnya*")
    
    # Overall Score
    rxlev_overall = safe_agg(op_data['Average RxLev (2G)']) if 'Average RxLev (2G)' in op_data.columns else np.nan
    rxqual_overall = safe_agg(op_data['Average RxQual (2G)']) if 'Average RxQual (2G)' in op_data.columns else np.nan
    score_overall = calculate_2g_score(rxlev_overall, rxqual_overall)
    badge_cls, badge_label = get_score_badge(score_overall)
    
    lines.append("")
    lines.append("---")
    lines.append(f"### 🎯 **Overall Score: <span class='{badge_cls} style='padding: 0.5rem 1rem;'>{badge_label} ({score_overall:.0f}/100)</span>**")
    
    return "\n".join(lines)

def generate_per_operator_conclusion_4g(df_data, operator):
    """Generate detailed 4G conclusion for specific operator"""
    lines = []
    lines.append(f"## 📊 **Kesimpulan 4G - {operator}**")
    lines.append("")
    
    op_data = df_data[df_data['Operator'] == operator]
    
    lines.append(f"**📅 Periode:** {op_data['Tanggal_Only'].min()} s/d {op_data['Tanggal_Only'].max()}")
    lines.append(f"**📍 Total Lokasi:** {op_data['Lokasi Pengukuran'].nunique()}")
    lines.append(f"**📊 Total Measurements:** {len(op_data)}")
    lines.append("")
    lines.append("---")
    
    # Overall Metrics
    lines.append("### 📈 **Overall Performance**")
    lines.append("")
    
    metrics_4g = [
        ('Average RSRP (Signal Strenght 4G)', 'RSRP', 'dBm', 'rsrp'),
        ('Average Speed Test DL (Mbps) (4G)', 'Download Speed', 'Mbps', 'speed'),
        ('Browsing Success (%)', 'Browsing Success Rate', '%', 'percentage'),
        ('Youtube SR (%)', 'YouTube Success Rate', '%', 'percentage')
    ]
    
    for col, label, unit, metric_type in metrics_4g:
        if col in op_data.columns:
            val_avg = safe_agg(op_data[col], 'mean')
            val_min = safe_agg(op_data[col], 'min')
            val_max = safe_agg(op_data[col], 'max')
            
            if pd.notna(val_avg):
                cat, cls = categorize_quality(val_avg, metric_type)
                lines.append(f"**{label}:**")
                lines.append(f"- Average: {val_avg:.2f} {unit} - <span class='{cls}'>{cat}</span>")
                lines.append(f"- Range: {val_min:.2f} to {val_max:.2f} {unit}")
                lines.append("")
    
    # Location Analysis
    lines.append("---")
    lines.append("### 📍 **Per Location Summary**")
    lines.append("")
    
    location_groups = op_data.groupby('Lokasi Pengukuran')
    for loc, loc_data in list(location_groups)[:5]:  # Top 5 locations
        rsrp_loc = safe_agg(loc_data['Average RSRP (Signal Strenght 4G)']) if 'Average RSRP (Signal Strenght 4G)' in loc_data.columns else np.nan
        speed_loc = safe_agg(loc_data['Average Speed Test DL (Mbps) (4G)']) if 'Average Speed Test DL (Mbps) (4G)' in loc_data.columns else np.nan
        browsing_loc = safe_agg(loc_data['Browsing Success (%)']) if 'Browsing Success (%)' in loc_data.columns else np.nan
        youtube_loc = safe_agg(loc_data['Youtube SR (%)']) if 'Youtube SR (%)' in loc_data.columns else np.nan
        
        score_loc = calculate_4g_score(rsrp_loc, speed_loc, browsing_loc, youtube_loc)
        badge_cls, badge_label = get_score_badge(score_loc)
        
        lines.append(f"**{loc}:**")
        if pd.notna(rsrp_loc):
            lines.append(f"- RSRP: {rsrp_loc:.2f} dBm")
        if pd.notna(speed_loc):
            lines.append(f"- DL Speed: {speed_loc:.2f} Mbps")
        lines.append(f"- Score: <span class='{badge_cls}'>{score_loc:.0f}/100</span>")
        lines.append("")
    
    if len(location_groups) > 5:
        lines.append(f"*...dan {len(location_groups) - 5} lokasi lainnya*")
    
    # Overall Score
    rsrp_overall = safe_agg(op_data['Average RSRP (Signal Strenght 4G)']) if 'Average RSRP (Signal Strenght 4G)' in op_data.columns else np.nan
    speed_overall = safe_agg(op_data['Average Speed Test DL (Mbps) (4G)']) if 'Average Speed Test DL (Mbps) (4G)' in op_data.columns else np.nan
    browsing_overall = safe_agg(op_data['Browsing Success (%)']) if 'Browsing Success (%)' in op_data.columns else np.nan
    youtube_overall = safe_agg(op_data['Youtube SR (%)']) if 'Youtube SR (%)' in op_data.columns else np.nan
    
    score_overall = calculate_4g_score(rsrp_overall, speed_overall, browsing_overall, youtube_overall)
    badge_cls, badge_label = get_score_badge(score_overall)
    
    lines.append("")
    lines.append("---")
    lines.append(f"### 🎯 **Overall Score: <span class='{badge_cls} style='padding: 0.5rem 1rem;'>{badge_label} ({score_overall:.0f}/100)</span>**")
    
    return "\n".join(lines)

# ===== DASHBOARD SECTIONS =====
def render_2g_dashboard_enhanced(df_filtered):
    """Enhanced 2G Dashboard with detailed information"""
    st.markdown('<div class="tech-mode-2g">📶 2G Technology - Enhanced Analysis</div>', unsafe_allow_html=True)
    
    has_2g = ('Average RxLev (2G)' in df_filtered.columns or 'Average RxQual (2G)' in df_filtered.columns)
    
    if not has_2g:
        st.warning("⚠️ Data 2G tidak tersedia dalam dataset")
        return
    
    # Overview
    st.markdown('<div class="section-header section-header-2g">📊 2G Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if 'Average RxLev (2G)' in df_filtered.columns:
            avg_rxlev = df_filtered['Average RxLev (2G)'].mean()
            st.metric("Avg RxLev", f"{avg_rxlev:.1f} dBm" if pd.notna(avg_rxlev) else "N/A")
    
    with col2:
        if 'Average RxQual (2G)' in df_filtered.columns:
            avg_rxqual = df_filtered['Average RxQual (2G)'].mean()
            st.metric("Avg RxQual", f"{avg_rxqual:.2f}" if pd.notna(avg_rxqual) else "N/A")
    
    with col3:
        st.metric("Locations", df_filtered['Lokasi Pengukuran'].nunique())
    
    with col4:
        st.metric("Operators", df_filtered['Operator'].nunique())
    
    with col5:
        st.metric("Measurements", len(df_filtered))
    
    # Detailed per Operator
    st.markdown('<div class="section-header section-header-2g">📈 Detailed 2G Metrics per Operator</div>', unsafe_allow_html=True)
    
    operators = sorted(df_filtered['Operator'].unique())
    
    for operator in operators:
        op_data = df_filtered[df_filtered['Operator'] == operator]
        render_2g_detailed_info(op_data, operator)
    
    # Charts
    st.markdown('<div class="section-header section-header-2g">📊 2G Performance Comparison</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📶 RxLev Analysis", "📡 RxQual Analysis"])
    
    with tab1:
        if 'Average RxLev (2G)' in df_filtered.columns:
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Average RxLev (2G)': lambda x: safe_agg(x)
            })
            fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                'Average RxLev (2G)', '2G RxLev by Location', chart_type='signal')
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        if 'Average RxQual (2G)' in df_filtered.columns:
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Average RxQual (2G)': lambda x: safe_agg(x)
            })
            fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                'Average RxQual (2G)', '2G RxQual by Location', chart_type='speed')
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    # Data Export
    st.markdown('<div class="section-header section-header-2g">📋 2G Data Export</div>', unsafe_allow_html=True)
    
    cols_2g = ['Operator', 'Lokasi Pengukuran', 'Tanggal_Only', 'Average RxLev (2G)', 'Average RxQual (2G)']
    display_cols = [c for c in cols_2g if c in df_filtered.columns]
    
    if display_cols:
        st.dataframe(df_filtered[display_cols].sort_values('Lokasi Pengukuran'), use_container_width=True, height=400)
        st.markdown(download_dataframe_as_excel(df_filtered[display_cols], "2G_Data.xlsx"), unsafe_allow_html=True)

def render_4g_dashboard(df_filtered):
    """4G Dashboard"""
    st.markdown('<div class="tech-mode-4g">📡 4G Technology Dashboard</div>', unsafe_allow_html=True)
    
    # Overview
    st.markdown('<div class="section-header section-header-4g">📊 4G Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'Average RSRP (Signal Strenght 4G)' in df_filtered.columns:
            avg_rsrp = df_filtered['Average RSRP (Signal Strenght 4G)'].mean()
            st.metric("Avg RSRP", f"{avg_rsrp:.1f} dBm" if pd.notna(avg_rsrp) else "N/A")
    
    with col2:
        if 'Average Speed Test DL (Mbps) (4G)' in df_filtered.columns:
            avg_dl = df_filtered['Average Speed Test DL (Mbps) (4G)'].mean()
            st.metric("Avg DL Speed", f"{avg_dl:.1f} Mbps" if pd.notna(avg_dl) else "N/A")
    
    with col3:
        if 'Youtube SR (%)' in df_filtered.columns:
            avg_yt = df_filtered['Youtube SR (%)'].mean()
            st.metric("YouTube SR", f"{avg_yt:.1f}%" if pd.notna(avg_yt) else "N/A")
    
    with col4:
        st.metric("Locations", df_filtered['Lokasi Pengukuran'].nunique())
    
    # Charts
    st.markdown('<div class="section-header section-header-4g">📈 4G Performance</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📡 Signal", "🚀 Speed", "📹 Services"])
    
    with tab1:
        if 'Average RSRP (Signal Strenght 4G)' in df_filtered.columns:
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Average RSRP (Signal Strenght 4G)': lambda x: safe_agg(x)
            })
            fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                'Average RSRP (Signal Strenght 4G)', '4G RSRP', chart_type='signal')
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
        col_a, col_b = st.columns(2)
        with col_a:
            if 'Browsing Success (%)' in df_filtered.columns:
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Browsing Success (%)': lambda x: safe_agg(x)
                })
                fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                    'Browsing Success (%)', 'Browsing Success Rate', chart_type='speed')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        with col_b:
            if 'Youtube SR (%)' in df_filtered.columns:
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Youtube SR (%)': lambda x: safe_agg(x)
                })
                fig = create_enhanced_chart(agg, 'Lokasi Pengukuran',
                    'Youtube SR (%)', 'YouTube Success Rate', chart_type='speed')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    # Data Export
    st.markdown('<div class="section-header section-header-4g">📋 4G Data Export</div>', unsafe_allow_html=True)
    
    cols_4g = ['Operator', 'Lokasi Pengukuran', 'Tanggal_Only', 
               'Average RSRP (Signal Strenght 4G)', 'Average Speed Test DL (Mbps) (4G)', 
               'Youtube SR (%)']
    display_cols = [c for c in cols_4g if c in df_filtered.columns]
    
    if display_cols:
        st.dataframe(df_filtered[display_cols].sort_values('Lokasi Pengukuran'), use_container_width=True, height=400)
        st.markdown(download_dataframe_as_excel(df_filtered[display_cols], "4G_Data.xlsx"), unsafe_allow_html=True)

def render_conclusions_menu(df_filtered, tech='2G'):
    """Dedicated conclusions menu"""
    st.markdown(f'<div class="section-header">📋 Menu Kesimpulan {tech}</div>', unsafe_allow_html=True)
    
    operators = sorted(df_filtered['Operator'].unique())
    
    conclusion_type = st.radio(
        "Pilih Jenis Kesimpulan:",
        ["📊 Overall (Semua Operator)", "👤 Per Operator"],
        horizontal=True,
        key=f'conclusion_type_{tech}'
    )
    
    st.markdown("---")
    
    if conclusion_type == "📊 Overall (Semua Operator)":
        st.markdown('<div class="conclusion-box">', unsafe_allow_html=True)
        
        if tech == '2G':
            conclusion = generate_overall_conclusion_2g(df_filtered, operators)
        else:
            conclusion = generate_overall_conclusion_4g(df_filtered, operators)
        
        st.markdown(conclusion, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:  # Per Operator
        selected_operator = st.selectbox(
            "Pilih Operator:",
            operators,
            key=f'operator_select_{tech}'
        )
        
        st.markdown('<div class="conclusion-box">', unsafe_allow_html=True)
        
        if tech == '2G':
            conclusion = generate_per_operator_conclusion_2g(df_filtered, selected_operator)
        else:
            conclusion = generate_per_operator_conclusion_4g(df_filtered, selected_operator)
        
        st.markdown(conclusion, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ===== MAIN APP =====
def main():
    st.markdown('<p class="main-header">📡 QoS Dashboard v2.0 - Enhanced</p>', unsafe_allow_html=True)
    
    # Sidebar
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
    
    # Load data
    with st.spinner('⏳ Loading data...'):
        df, error = load_and_prepare_data(file_path)
    
    if error:
        st.error(f"❌ {error}")
        return
    
    if df is None or len(df) == 0:
        st.error("❌ No data available")
        return
    
    # Sidebar Filters
    with st.sidebar:
        st.markdown("---")
        st.title("🔍 Filters")
        
        # Kabupaten Filter
        kab_opts = ['All'] + sorted([str(k) for k in df['Kabupaten / Kota'].unique() if pd.notna(k)])
        sel_kab = st.selectbox("📍 Kabupaten", kab_opts, key='kab_filter')
        
        df_filtered = df.copy()
        if sel_kab != 'All':
            df_filtered = df_filtered[df_filtered['Kabupaten / Kota'] == sel_kab]
        
        # MULTI-DATE FILTER (NEW!)
        has_date = 'Tanggal_Only' in df_filtered.columns and df_filtered['Tanggal_Only'].notna().any()
        
        if has_date:
            st.markdown("**📅 Date Filter** ⭐ **Multi-Select!**")
            
            date_filter_mode = st.radio(
                "Mode:",
                ["All Dates", "Date Range", "Multiple Dates"],
                key='date_filter_mode',
                horizontal=True
            )
            
            if date_filter_mode == "Date Range":
                dates = sorted(df_filtered['Tanggal_Only'].dropna().unique())
                min_date = min(dates)
                max_date = max(dates)
                
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("From", min_date, key='start_date')
                with col2:
                    end_date = st.date_input("To", max_date, key='end_date')
                
                df_filtered = df_filtered[
                    (df_filtered['Tanggal_Only'] >= start_date) & 
                    (df_filtered['Tanggal_Only'] <= end_date)
                ]
                
                days_diff = (end_date - start_date).days + 1
                st.success(f"✅ {days_diff} days selected")
            
            elif date_filter_mode == "Multiple Dates":
                dates = sorted(df_filtered['Tanggal_Only'].dropna().unique())
                
                selected_dates = st.multiselect(
                    "Select Dates:",
                    dates,
                    format_func=lambda x: pd.to_datetime(x).strftime('%d %B %Y'),
                    key='multi_date_select'
                )
                
                if selected_dates:
                    df_filtered = df_filtered[df_filtered['Tanggal_Only'].isin(selected_dates)]
                    st.success(f"✅ {len(selected_dates)} date(s) selected")
                else:
                    st.info("💡 Select at least one date")
        
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
        
        if has_date and not df_filtered.empty:
            col1, col2 = st.columns(2)
            col1.metric("📅 Dates", f"{df_filtered['Tanggal_Only'].nunique()}")
            col2.metric("👥 Operators", df_filtered['Operator'].nunique())
    
    if df_filtered.empty:
        st.warning("⚠️ No data matches the selected filters")
        return
    
    # Main Dashboard
    st.markdown("---")
    
    # Dashboard Mode Selection
    dashboard_mode = st.radio(
        "📡 **Select Dashboard View**",
        ["📶 2G Analysis", "📡 4G Analysis", "📋 Kesimpulan 2G", "📋 Kesimpulan 4G"],
        horizontal=True,
        key='dashboard_mode'
    )
    
    st.markdown("---")
    
    if dashboard_mode == "📶 2G Analysis":
        render_2g_dashboard_enhanced(df_filtered)
    
    elif dashboard_mode == "📡 4G Analysis":
        render_4g_dashboard(df_filtered)
    
    elif dashboard_mode == "📋 Kesimpulan 2G":
        render_conclusions_menu(df_filtered, tech='2G')
    
    elif dashboard_mode == "📋 Kesimpulan 4G":
        render_conclusions_menu(df_filtered, tech='4G')
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #7f8c8d; padding: 2rem 0;'>
            <p style='font-size: 1rem;'>📡 <strong>QoS Dashboard v2.0</strong></p>
            <p style='font-size: 0.9rem;'>Multi-Date Filter | Enhanced 2G Info | Dedicated Conclusion Menu</p>
            <p style='font-size: 0.8rem;'>✨ Powered by Streamlit & Plotly</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()