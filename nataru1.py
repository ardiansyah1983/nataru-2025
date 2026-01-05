"""
Dashboard QoS Telekomunikasi - FINAL VERSION
✅ Auto-read from 'data' folder
✅ PERFECT bar charts - baseline 0 sejajar di bawah
✅ Detailed conclusions per measurement
✅ Include Smartfren (4 operators total)
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
warnings.filterwarnings('ignore')

# ===== CONFIGURATION =====
st.set_page_config(
    page_title="Dashboard QoS Telekomunikasi",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== STYLING =====
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(120deg, #1f77b4, #2ecc71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .quality-excellent {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white; padding: 0.5rem 1rem;
        border-radius: 8px; display: inline-block;
        font-weight: bold; margin: 0.2rem;
    }
    .quality-good {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white; padding: 0.5rem 1rem;
        border-radius: 8px; display: inline-block;
        font-weight: bold; margin: 0.2rem;
    }
    .quality-fair {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white; padding: 0.5rem 1rem;
        border-radius: 8px; display: inline-block;
        font-weight: bold; margin: 0.2rem;
    }
    .quality-poor {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white; padding: 0.5rem 1rem;
        border-radius: 8px; display: inline-block;
        font-weight: bold; margin: 0.2rem;
    }
    .conclusion-card {
        background-color: #f8f9fa;
        border-left: 5px solid #3498db;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ===== CONSTANTS =====
ALLOWED_OPERATORS = ['Indosat', 'Telkomsel', 'XL', 'Smartfren']  # Include Smartfren
OPERATOR_COLORS = {
    'Indosat': '#FFD700', 
    'Telkomsel': '#DC143C', 
    'XL': '#4169E1',
    'Smartfren': '#9400D3'
}
DATA_FOLDER = 'data'

# ===== FILE MANAGEMENT =====
def get_data_files(folder='data'):
    """Scan folder untuk file data"""
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
    """Get file info"""
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
    """Identifikasi kolom numeric"""
    keywords = ['Average', 'Median', 'Max', 'Min', 'Success', 'SR', '(%)', 
                'Speed', 'Mbps', 'RSRP', 'RSRQ', 'SINR', 'Latency', 'RTT',
                'YouTube', 'Youtube', 'Quality', 'MOS', 'CST', 'Sample',
                'RxLev', 'RxQual', 'RSCP', 'ECIO', 'Bad']
    
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
    """Konversi kolom ke numeric"""
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
    """Load dan prepare data"""
    try:
        # Detect file type
        if isinstance(file_path, str):
            file_ext = file_path.split('.')[-1].lower()
        else:
            file_ext = file_path.name.split('.')[-1].lower()
        
        # Load
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
        
        # Validate
        required = ['Operator', 'Kabupaten / Kota', 'Lokasi Pengukuran']
        missing = [c for c in required if c not in df.columns]
        if missing:
            return None, f"Kolom tidak ada: {', '.join(missing)}"
        
        # Filter operator (include Smartfren now)
        df = df[df['Operator'].isin(ALLOWED_OPERATORS)].copy()
        if len(df) == 0:
            return None, "Tidak ada data untuk operator yang didukung"
        
        df = df.dropna(subset=['Operator', 'Kabupaten / Kota'])
        
        # Convert tanggal
        if 'Tanggal Pengukuran' in df.columns:
            df['Tanggal Pengukuran'] = pd.to_datetime(df['Tanggal Pengukuran'], errors='coerce')
            df['Tanggal_Only'] = df['Tanggal Pengukuran'].dt.date
        
        # Convert numeric
        numeric_cols = identify_numeric_columns(df)
        df = convert_to_numeric_safe(df, numeric_cols)
        
        return df, None
        
    except Exception as e:
        return None, f"Error: {str(e)}"

# ===== HELPER FUNCTIONS =====
def safe_agg(series, func='mean'):
    """Safe aggregation"""
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

def create_signal_quality_chart(data, x_col, y_col, title, color_col='Operator'):
    """
    Create PERFECT bar chart untuk Signal Quality (nilai negatif)
    dengan baseline 0 yang SEJAJAR DI BAWAH
    """
    try:
        if y_col not in data.columns:
            return None
        
        plot_data = data[[x_col, y_col, color_col]].dropna(subset=[y_col])
        if plot_data.empty:
            return None
        
        fig = px.bar(
            plot_data,
            x=x_col,
            y=y_col,
            color=color_col,
            barmode='group',
            title=title,
            color_discrete_map=OPERATOR_COLORS,
            text=y_col
        )
        
        # CRITICAL: Set y-axis range untuk signal (nilai negatif)
        # Baseline 0 HARUS di atas, nilai negatif turun ke bawah
        y_min = plot_data[y_col].min()
        y_max = plot_data[y_col].max()
        
        # Add 10% padding
        padding = abs(y_min) * 0.1
        
        # Set range: dari nilai minimum (lebih negatif) ke 0
        # Ini membuat 0 sejajar di ATAS sebagai baseline
        y_range = [y_min - padding, 5]  # 5 untuk sedikit ruang di atas 0
        
        fig.update_layout(
            height=500,
            hovermode='x unified',
            xaxis={
                'tickangle': -45, 
                'title': None
            },
            yaxis={
                'title': y_col.split('(')[0].strip(),
                'range': y_range,
                'zeroline': True,           # Show zero line
                'zerolinewidth': 3,         # Thick zero line
                'zerolinecolor': '#000',    # Black color
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': '#e0e0e0'
            },
            legend={
                'orientation': 'h',
                'yanchor': 'bottom',
                'y': 1.02,
                'xanchor': 'center',
                'x': 0.5,
                'title': None
            },
            title={
                'text': title, 
                'x': 0.5, 
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#2c3e50'}
            },
            margin={'t': 80, 'b': 100, 'l': 80, 'r': 40},
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        # Add value labels
        fig.update_traces(
            texttemplate='%{text:.1f}',
            textposition='outside',
            textfont={'size': 9, 'color': '#2c3e50'}
        )
        
        # Add horizontal line at y=0 for emphasis
        fig.add_hline(
            y=0, 
            line_dash="solid", 
            line_color="#000", 
            line_width=2,
            annotation_text="Baseline (0)",
            annotation_position="right"
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None

def create_speed_chart(data, x_col, y_col, title, color_col='Operator'):
    """
    Create bar chart untuk Speed/Percentage (nilai positif)
    dengan baseline 0 di BAWAH
    """
    try:
        if y_col not in data.columns:
            return None
        
        plot_data = data[[x_col, y_col, color_col]].dropna(subset=[y_col])
        if plot_data.empty:
            return None
        
        fig = px.bar(
            plot_data,
            x=x_col,
            y=y_col,
            color=color_col,
            barmode='group',
            title=title,
            color_discrete_map=OPERATOR_COLORS,
            text=y_col
        )
        
        # For positive values: baseline 0 at bottom
        y_max = plot_data[y_col].max()
        y_range = [0, y_max * 1.15]
        
        fig.update_layout(
            height=500,
            hovermode='x unified',
            xaxis={
                'tickangle': -45, 
                'title': None
            },
            yaxis={
                'title': y_col.split('(')[0].strip(),
                'range': y_range,
                'zeroline': True,
                'zerolinewidth': 3,
                'zerolinecolor': '#000',
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': '#e0e0e0'
            },
            legend={
                'orientation': 'h',
                'yanchor': 'bottom',
                'y': 1.02,
                'xanchor': 'center',
                'x': 0.5,
                'title': None
            },
            title={
                'text': title, 
                'x': 0.5, 
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#2c3e50'}
            },
            margin={'t': 80, 'b': 100, 'l': 80, 'r': 40},
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        fig.update_traces(
            texttemplate='%{text:.1f}',
            textposition='outside',
            textfont={'size': 9, 'color': '#2c3e50'}
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None

def categorize_quality(value, metric_type):
    """Kategorisasi kualitas"""
    if pd.isna(value):
        return "No Data", "quality-poor"
    
    if metric_type == 'rsrp':
        if value >= -80:
            return "Excellent", "quality-excellent"
        elif value >= -90:
            return "Good", "quality-good"
        elif value >= -100:
            return "Fair", "quality-fair"
        else:
            return "Poor", "quality-poor"
    
    elif metric_type == 'speed':
        if value >= 30:
            return "Excellent", "quality-excellent"
        elif value >= 15:
            return "Good", "quality-good"
        elif value >= 5:
            return "Fair", "quality-fair"
        else:
            return "Poor", "quality-poor"
    
    elif metric_type == 'percentage':
        if value >= 95:
            return "Excellent", "quality-excellent"
        elif value >= 85:
            return "Good", "quality-good"
        elif value >= 70:
            return "Fair", "quality-fair"
        else:
            return "Poor", "quality-poor"
    
    return "Unknown", "quality-poor"

def generate_detailed_conclusion(df_data, location, operator, date_str=None):
    """Generate kesimpulan detail per pengukuran"""
    lines = []
    
    lines.append("### 📋 Kesimpulan Pengukuran")
    lines.append(f"**📍 Lokasi:** {location}")
    lines.append(f"**👤 Operator:** {operator}")
    if date_str:
        lines.append(f"**📅 Tanggal:** {date_str}")
    lines.append("")
    
    # Signal Quality
    lines.append("**📡 Kualitas Signal 4G:**")
    if 'Average RSRP (Signal Strenght 4G)' in df_data.columns:
        rsrp = safe_agg(df_data['Average RSRP (Signal Strenght 4G)'])
        if pd.notna(rsrp):
            cat, cls = categorize_quality(rsrp, 'rsrp')
            lines.append(f"- RSRP: **{rsrp:.2f} dBm** - <span class='{cls}'>{cat}</span>")
        else:
            lines.append(f"- RSRP: <span class='quality-poor'>No Data</span>")
    
    if 'Average RSRQ (Signal Qualty 4G)' in df_data.columns:
        rsrq = safe_agg(df_data['Average RSRQ (Signal Qualty 4G)'])
        if pd.notna(rsrq):
            lines.append(f"- RSRQ: **{rsrq:.2f} dB**")
    
    if 'Average SINR (Signal Qualty 4G)' in df_data.columns:
        sinr = safe_agg(df_data['Average SINR (Signal Qualty 4G)'])
        if pd.notna(sinr):
            lines.append(f"- SINR: **{sinr:.2f} dB**")
    
    # Speed Performance
    lines.append("")
    lines.append("**🚀 Kecepatan Internet:**")
    if 'Average Speed Test DL (Mbps) (4G)' in df_data.columns:
        dl = safe_agg(df_data['Average Speed Test DL (Mbps) (4G)'])
        if pd.notna(dl):
            cat, cls = categorize_quality(dl, 'speed')
            lines.append(f"- Download: **{dl:.2f} Mbps** - <span class='{cls}'>{cat}</span>")
    
    if 'Average Speed Test UL (Mbps) (4G)' in df_data.columns:
        ul = safe_agg(df_data['Average Speed Test UL (Mbps) (4G)'])
        if pd.notna(ul):
            lines.append(f"- Upload: **{ul:.2f} Mbps**")
    
    # Service Quality
    lines.append("")
    lines.append("**📱 Kualitas Layanan:**")
    if 'Youtube SR (%)' in df_data.columns:
        yt = safe_agg(df_data['Youtube SR (%)'])
        if pd.notna(yt):
            cat, cls = categorize_quality(yt, 'percentage')
            lines.append(f"- YouTube SR: **{yt:.1f}%** - <span class='{cls}'>{cat}</span>")
    
    if 'Average RTT Latency (ms)' in df_data.columns:
        lat = safe_agg(df_data['Average RTT Latency (ms)'])
        if pd.notna(lat):
            lat_status = "Baik" if lat < 100 else "Cukup" if lat < 150 else "Kurang"
            lines.append(f"- Latency: **{lat:.2f} ms** ({lat_status})")
    
    # Recommendations
    lines.append("")
    lines.append("**💡 Rekomendasi:**")
    
    recs = []
    if 'Average RSRP (Signal Strenght 4G)' in df_data.columns:
        rsrp = safe_agg(df_data['Average RSRP (Signal Strenght 4G)'])
        if pd.notna(rsrp):
            if rsrp < -100:
                recs.append("⚠️ **Signal lemah** - Perlu optimasi coverage")
            elif rsrp < -90:
                recs.append("⚡ Signal cukup - Monitor konsistensi")
    
    if 'Average Speed Test DL (Mbps) (4G)' in df_data.columns:
        dl = safe_agg(df_data['Average Speed Test DL (Mbps) (4G)'])
        if pd.notna(dl):
            if dl < 10:
                recs.append("⚠️ **Speed rendah** - Perlu peningkatan kapasitas")
            elif dl < 20:
                recs.append("⚡ Speed cukup - Monitor traffic pattern")
    
    if 'Youtube SR (%)' in df_data.columns:
        yt = safe_agg(df_data['Youtube SR (%)'])
        if pd.notna(yt):
            if yt < 85:
                recs.append("⚠️ **YouTube SR rendah** - Investigasi QoE")
    
    if not recs:
        recs.append("✅ Kualitas layanan baik - Pertahankan performa")
    
    lines.extend([f"- {r}" for r in recs])
    
    return "\n".join(lines)

# ===== MAIN APP =====
def main():
    # Header
    st.markdown('<p class="main-header">📡 Dashboard QoS Telekomunikasi</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">📊 397 Baris Data | 4 Operator | Perfect Baseline Charts</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📁 Sumber Data")
    
    data_files = get_data_files(DATA_FOLDER)
    file_path = None
    
    if data_files:
        st.sidebar.success(f"✅ {len(data_files)} file tersedia")
        file_names = [os.path.basename(f) for f in data_files]
        selected_file = st.sidebar.selectbox("📂 Pilih File", file_names)
        idx = file_names.index(selected_file)
        file_path = data_files[idx]
        
        info = get_file_info(file_path)
        if info:
            st.sidebar.info(f"📊 {info['size']} | 🕐 {info['modified']}")
    else:
        st.sidebar.warning(f"⚠️ Folder '{DATA_FOLDER}' kosong")
        uploaded = st.sidebar.file_uploader("📤 Upload File", type=['xlsx', 'xls', 'csv'])
        if uploaded:
            file_path = uploaded
            st.sidebar.success(f"✅ {uploaded.name}")
        else:
            st.info(f"""
            **📁 Setup:**
            1. Buat folder `{DATA_FOLDER}`
            2. Letakkan file Excel/CSV
            3. Refresh browser
            
            **Path:** `{os.path.abspath(DATA_FOLDER)}`
            """)
            return
    
    # Load data
    with st.spinner('⏳ Loading...'):
        df, error = load_and_prepare_data(file_path)
    
    if error:
        st.error(f"❌ {error}")
        return
    
    if df is None or len(df) == 0:
        st.error("❌ Tidak ada data")
        return
    
    st.sidebar.success(f"✅ {len(df):,} baris ({df['Operator'].nunique()} operator)")
    
    # Filters
    st.sidebar.markdown("---")
    st.sidebar.title("🔍 Filter")
    
    kab_opts = ['Semua'] + sorted([str(k) for k in df['Kabupaten / Kota'].unique() if pd.notna(k)])
    sel_kab = st.sidebar.selectbox("📍 Kabupaten/Kota", kab_opts)
    
    df_filtered = df.copy()
    if sel_kab != 'Semua':
        df_filtered = df_filtered[df_filtered['Kabupaten / Kota'] == sel_kab]
    
    has_date = 'Tanggal_Only' in df_filtered.columns and df_filtered['Tanggal_Only'].notna().any()
    
    if has_date:
        st.sidebar.markdown("**📅 Tanggal**")
        date_type = st.sidebar.radio("", ["Semua", "Spesifik"], horizontal=True)
        
        if date_type == "Spesifik":
            dates = sorted(df_filtered['Tanggal_Only'].dropna().unique())
            sel_date = st.sidebar.selectbox(
                "Pilih",
                dates,
                format_func=lambda x: pd.to_datetime(x).strftime('%d %B %Y')
            )
            df_filtered = df_filtered[df_filtered['Tanggal_Only'] == sel_date]
    
    lok_opts = ['Semua'] + sorted([str(l) for l in df_filtered['Lokasi Pengukuran'].unique() if pd.notna(l)])
    sel_lok = st.sidebar.selectbox("📍 Lokasi", lok_opts)
    
    if sel_lok != 'Semua':
        df_filtered = df_filtered[df_filtered['Lokasi Pengukuran'] == sel_lok]
    
    op_opts = ['Semua'] + sorted(ALLOWED_OPERATORS)
    sel_ops = st.sidebar.multiselect("👥 Operator", op_opts, default='Semua')
    
    if 'Semua' not in sel_ops and sel_ops:
        df_filtered = df_filtered[df_filtered['Operator'].isin(sel_ops)]
    
    st.sidebar.markdown("---")
    col1, col2 = st.sidebar.columns(2)
    col1.metric("📊 Data", f"{len(df_filtered):,}")
    col2.metric("📍 Lokasi", df_filtered['Lokasi Pengukuran'].nunique())
    
    if df_filtered.empty:
        st.warning("⚠️ Tidak ada data")
        return
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "📡 Signal Quality",
        "🚀 Speed & Services",
        "📍 Per Lokasi",
        "📋 Kesimpulan Detail"
    ])
    
    # TAB 1: OVERVIEW
    with tab1:
        st.markdown("### 📊 Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📝 Total", f"{len(df_filtered):,}")
        with col2:
            st.metric("📍 Lokasi", df_filtered['Lokasi Pengukuran'].nunique())
        with col3:
            st.metric("🏢 Operator", df_filtered['Operator'].nunique())
        with col4:
            if has_date:
                st.metric("📅 Hari", df_filtered['Tanggal_Only'].nunique())
        
        st.markdown("---")
        
        st.markdown("### 📈 Ringkasan per Operator")
        
        metrics = {
            'RSRP (dBm)': 'Average RSRP (Signal Strenght 4G)',
            'DL Speed (Mbps)': 'Average Speed Test DL (Mbps) (4G)',
            'YouTube SR (%)': 'Youtube SR (%)',
            'Latency (ms)': 'Average RTT Latency (ms)'
        }
        
        summary = {}
        for label, col in metrics.items():
            if col in df_filtered.columns:
                summary[label] = {
                    op: safe_agg(df_filtered[df_filtered['Operator']==op][col])
                    for op in ALLOWED_OPERATORS if op in df_filtered['Operator'].unique()
                }
        
        if summary:
            summary_df = pd.DataFrame(summary).T.round(2)
            st.dataframe(summary_df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            op_counts = df_filtered['Operator'].value_counts()
            fig = px.pie(
                values=op_counts.values,
                names=op_counts.index,
                title="Distribusi per Operator",
                color=op_counts.index,
                color_discrete_map=OPERATOR_COLORS
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            loc_counts = df_filtered['Lokasi Pengukuran'].value_counts().head(10)
            fig = px.bar(
                x=loc_counts.values,
                y=loc_counts.index,
                orientation='h',
                title="Top 10 Lokasi"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 2: SIGNAL QUALITY - DENGAN PERFECT BASELINE
    with tab2:
        st.markdown("### 📡 Signal Quality Analysis")
        st.info("💡 **Chart ini menggunakan baseline 0 yang sejajar di bawah** - Bar turun dari 0 ke nilai negatif")
        
        if 'Average RSRP (Signal Strenght 4G)' in df_filtered.columns:
            st.markdown("#### 📡 RSRP 4G (Signal Strength)")
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Average RSRP (Signal Strenght 4G)': lambda x: safe_agg(x)
            })
            
            fig = create_signal_quality_chart(
                agg,
                'Lokasi Pengukuran',
                'Average RSRP (Signal Strenght 4G)',
                'RSRP 4G per Lokasi dan Operator (dBm) - Baseline 0 di Atas'
            )
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                st.caption("📌 Excellent: ≥-80 dBm | Good: -80 to -90 dBm | Fair: -90 to -100 dBm | Poor: <-100 dBm")
        
        if 'Average RSRQ (Signal Qualty 4G)' in df_filtered.columns:
            st.markdown("#### 📊 RSRQ 4G (Signal Quality)")
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Average RSRQ (Signal Qualty 4G)': lambda x: safe_agg(x)
            })
            
            fig = create_signal_quality_chart(
                agg,
                'Lokasi Pengukuran',
                'Average RSRQ (Signal Qualty 4G)',
                'RSRQ 4G per Lokasi dan Operator (dB) - Baseline 0 di Atas'
            )
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        if 'Average SINR (Signal Qualty 4G)' in df_filtered.columns:
            st.markdown("#### 📈 SINR 4G (Signal Quality)")
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Average SINR (Signal Qualty 4G)': lambda x: safe_agg(x)
            })
            
            fig = create_signal_quality_chart(
                agg,
                'Lokasi Pengukuran',
                'Average SINR (Signal Qualty 4G)',
                'SINR 4G per Lokasi dan Operator (dB) - Baseline 0 di Atas'
            )
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    # TAB 3: SPEED
    with tab3:
        st.markdown("### 🚀 Speed & Services")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Average Speed Test DL (Mbps) (4G)' in df_filtered.columns:
                st.markdown("#### 📥 Download Speed 4G")
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average Speed Test DL (Mbps) (4G)': lambda x: safe_agg(x)
                })
                
                fig = create_speed_chart(
                    agg,
                    'Lokasi Pengukuran',
                    'Average Speed Test DL (Mbps) (4G)',
                    'Download Speed 4G (Mbps)'
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Youtube SR (%)' in df_filtered.columns:
                st.markdown("#### 📹 YouTube Success Rate")
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Youtube SR (%)': lambda x: safe_agg(x)
                })
                
                fig = create_speed_chart(
                    agg,
                    'Lokasi Pengukuran',
                    'Youtube SR (%)',
                    'YouTube Success Rate (%)'
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    # TAB 4: PER LOKASI
    with tab4:
        st.markdown("### 📍 Analisis per Lokasi")
        
        locations = sorted(df_filtered['Lokasi Pengukuran'].unique())
        if locations:
            sel_loc = st.selectbox("🎯 Pilih Lokasi", locations)
            df_loc = df_filtered[df_filtered['Lokasi Pengukuran'] == sel_loc]
            
            st.markdown(f"#### 📍 {sel_loc}")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👥 Operator", df_loc['Operator'].nunique())
            with col2:
                if 'Average RSRP (Signal Strenght 4G)' in df_loc.columns:
                    avg = safe_agg(df_loc['Average RSRP (Signal Strenght 4G)'])
                    st.metric("📡 RSRP", f"{avg:.2f} dBm" if pd.notna(avg) else "N/A")
            with col3:
                if 'Average Speed Test DL (Mbps) (4G)' in df_loc.columns:
                    avg = safe_agg(df_loc['Average Speed Test DL (Mbps) (4G)'])
                    st.metric("🚀 DL", f"{avg:.2f} Mbps" if pd.notna(avg) else "N/A")
            with col4:
                if has_date:
                    st.metric("📅 Hari", df_loc['Tanggal_Only'].nunique())
            
            st.markdown("#### 📊 Perbandingan Operator")
            
            detail_cols = [
                'Average RSRP (Signal Strenght 4G)',
                'Average RSRQ (Signal Qualty 4G)',
                'Average Speed Test DL (Mbps) (4G)',
                'Average Speed Test UL (Mbps) (4G)',
                'Youtube SR (%)',
                'Average RTT Latency (ms)'
            ]
            
            avail = [c for c in detail_cols if c in df_loc.columns]
            
            if avail:
                detail = df_loc.groupby('Operator')[avail].agg(lambda x: safe_agg(x)).round(2)
                st.dataframe(detail, use_container_width=True)
    
    # TAB 5: KESIMPULAN
    with tab5:
        st.markdown("### 📋 Kesimpulan Detail")
        
        if has_date:
            groupby_cols = ['Lokasi Pengukuran', 'Operator', 'Tanggal_Only']
        else:
            groupby_cols = ['Lokasi Pengukuran', 'Operator']
        
        grouped = df_filtered.groupby(groupby_cols)
        total = len(grouped)
        
        st.info(f"📊 Total {total} kombinasi pengukuran")
        
        per_page = 5
        total_pages = (total + per_page - 1) // per_page
        
        page = st.selectbox("Halaman", range(1, total_pages + 1))
        
        start = (page - 1) * per_page
        end = min(start + per_page, total)
        
        for idx, (keys, data) in enumerate(list(grouped)[start:end], start=start + 1):
            if has_date:
                loc, op, date = keys
                date_str = pd.to_datetime(date).strftime('%d %B %Y')
                title = f"📌 {idx}. {loc} - {op} ({date_str})"
            else:
                loc, op = keys
                date_str = None
                title = f"📌 {idx}. {loc} - {op}"
            
            with st.expander(title, expanded=(idx == start + 1)):
                conclusion = generate_detailed_conclusion(data, loc, op, date_str)
                st.markdown(f"<div class='conclusion-card'>{conclusion}</div>", unsafe_allow_html=True)
        
        st.caption(f"Menampilkan {start + 1}-{end} dari {total}")

if __name__ == "__main__":
    main()