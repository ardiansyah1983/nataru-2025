"""
Dashboard QoS Telekomunikasi - Version 5.0 (Auto-Read from Folder)
Auto-detect & load files from 'data' folder
Support: .xlsx, .xls, .csv
Operators: Indosat, Telkomsel, XL
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import glob
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
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        padding: 0.5rem 0;
    }
    .file-info {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .conclusion-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2ecc71;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ===== CONSTANTS =====
ALLOWED_OPERATORS = ['Indosat', 'Telkomsel', 'XL']
OPERATOR_COLORS = {
    'Indosat': '#FFD700',
    'Telkomsel': '#DC143C',
    'XL': '#4169E1'
}

DATA_FOLDER = 'data'

# ===== FILE MANAGEMENT FUNCTIONS =====

def get_data_files(folder='data'):
    """Scan folder untuk file data (.xlsx, .xls, .csv)"""
    if not os.path.exists(folder):
        os.makedirs(folder)
        return []
    
    # Cari semua file dengan ekstensi yang didukung
    patterns = ['*.xlsx', '*.xls', '*.csv']
    files = []
    
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(folder, pattern)))
    
    # Sort by modification time (newest first)
    files.sort(key=os.path.getmtime, reverse=True)
    
    return files

def get_file_info(filepath):
    """Get informasi file"""
    if not os.path.exists(filepath):
        return None
    
    stat = os.stat(filepath)
    size_mb = stat.st_size / (1024 * 1024)
    
    from datetime import datetime
    mod_time = datetime.fromtimestamp(stat.st_mtime)
    
    return {
        'name': os.path.basename(filepath),
        'size': f"{size_mb:.2f} MB",
        'modified': mod_time.strftime('%Y-%m-%d %H:%M:%S'),
        'path': filepath
    }

# ===== DATA LOADING FUNCTIONS =====

def identify_numeric_columns(df):
    """Identifikasi semua kolom yang seharusnya numeric"""
    numeric_keywords = [
        'Average', 'Median', 'Max', 'Min', 'Total', 'Count',
        'Success', 'SR', '(%)', 'Speed', 'Mbps', 'ms',
        'RSRP', 'RSRQ', 'SINR', 'RxLev', 'RxQual', 'RSCP', 'ECIO',
        'MOS', 'CST', 'TTFP', 'Latency', 'RTT', 'Quality',
        'Bad', 'Sample', 'Blocked', 'Dropped', 'Packet', 'Loss',
        'Rank', 'Attempts', 'FTP', 'DL', 'UL', 'Browsing',
        'Capacity', 'Ping', 'Video', 'Call', 'SMS', 'Message',
        'Freezing', 'Jerkiness', 'Visual', 'YouTube', 'Youtube',
        'WA ', 'Duration', 'Receive', 'Send'
    ]
    
    numeric_cols = []
    for col in df.columns:
        col_str = str(col)
        # Skip kolom yang jelas non-numeric
        if col_str in ['No.', 'Zona', 'Kode Kabupaten / Kota', 'Kabupaten / Kota', 
                       'Jenis Tes', 'POI', 'Kecamatan', 'Desa', 'Lokasi Pengukuran',
                       'Event', 'Kecamatan > 1 (Ya/Tidak)', 'Tanggal Pengukuran', 
                       'Operator', 'Category', 'Lokasi POI', 'Keterangan',
                       'Probe Name', 'Test Type', 'Campign Name', 'Network Technology']:
            continue
        
        # Check keyword
        for keyword in numeric_keywords:
            if keyword in col_str:
                numeric_cols.append(col)
                break
    
    return numeric_cols

def convert_to_numeric_safe(df, columns):
    """Konversi kolom ke numeric dengan aman"""
    df_copy = df.copy()
    
    for col in columns:
        if col in df_copy.columns:
            try:
                # Replace non-numeric values
                df_copy[col] = df_copy[col].replace({
                    'No Data': np.nan,
                    'no data': np.nan,
                    'N/A': np.nan,
                    'n/a': np.nan,
                    '-': np.nan,
                    '': np.nan,
                    ' ': np.nan
                })
                
                # Convert
                df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')
            except:
                df_copy[col] = np.nan
    
    return df_copy

@st.cache_data(show_spinner=False)
def load_and_prepare_data(file_path):
    """Load dan prepare data dengan konversi lengkap"""
    try:
        # Detect file type
        file_ext = file_path.split('.')[-1].lower()
        
        # Load data
        if file_ext == 'xlsx':
            try:
                df = pd.read_excel(file_path, sheet_name='Compile_Summary', engine='openpyxl')
            except:
                # Try reading all sheets
                xl = pd.ExcelFile(file_path)
                if 'Compile_Summary' in xl.sheet_names:
                    df = pd.read_excel(file_path, sheet_name='Compile_Summary', engine='openpyxl')
                else:
                    # Use first sheet
                    df = pd.read_excel(file_path, sheet_name=0, engine='openpyxl')
        elif file_ext == 'xls':
            try:
                df = pd.read_excel(file_path, sheet_name='Compile_Summary', engine='xlrd')
            except:
                xl = pd.ExcelFile(file_path, engine='xlrd')
                if 'Compile_Summary' in xl.sheet_names:
                    df = pd.read_excel(file_path, sheet_name='Compile_Summary', engine='xlrd')
                else:
                    df = pd.read_excel(file_path, sheet_name=0, engine='xlrd')
        elif file_ext == 'csv':
            df = pd.read_csv(file_path)
        else:
            return None, f"Format tidak didukung: {file_ext}"
        
        # Validasi kolom required
        required = ['Operator', 'Kabupaten / Kota', 'Lokasi Pengukuran']
        missing = [col for col in required if col not in df.columns]
        if missing:
            return None, f"Kolom tidak ditemukan: {', '.join(missing)}"
        
        # Filter operator
        df = df[df['Operator'].isin(ALLOWED_OPERATORS)].copy()
        if len(df) == 0:
            return None, "Tidak ada data untuk Indosat, Telkomsel, atau XL"
        
        # Drop rows tanpa data penting
        df = df.dropna(subset=['Operator', 'Kabupaten / Kota'])
        
        # Convert tanggal
        if 'Tanggal Pengukuran' in df.columns:
            df['Tanggal Pengukuran'] = pd.to_datetime(df['Tanggal Pengukuran'], errors='coerce')
            df['Tahun'] = df['Tanggal Pengukuran'].dt.year
            df['Bulan'] = df['Tanggal Pengukuran'].dt.month
        elif 'Tanggal' in df.columns:
            df['Tanggal Pengukuran'] = pd.to_datetime(df['Tanggal'], errors='coerce')
            df['Tahun'] = df['Tanggal Pengukuran'].dt.year
            df['Bulan'] = df['Tanggal Pengukuran'].dt.month
        
        # Identify dan convert numeric columns
        numeric_cols = identify_numeric_columns(df)
        df = convert_to_numeric_safe(df, numeric_cols)
        
        return df, None
        
    except Exception as e:
        return None, f"Error loading data: {str(e)}"

# ===== HELPER FUNCTIONS =====

def safe_agg(series, func='mean'):
    """Safe aggregation dengan NaN handling"""
    try:
        if func == 'mean':
            return series.mean() if series.notna().any() else np.nan
        elif func == 'sum':
            return series.sum() if series.notna().any() else np.nan
        elif func == 'min':
            return series.min() if series.notna().any() else np.nan
        elif func == 'max':
            return series.max() if series.notna().any() else np.nan
        elif func == 'count':
            return series.notna().sum()
        else:
            return np.nan
    except:
        return np.nan

def create_bar_chart(data, x_col, y_col, title, color_col='Operator'):
    """Create bar chart dengan error handling"""
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
            color_discrete_map=OPERATOR_COLORS
        )
        
        fig.update_layout(
            height=500,
            hovermode='x unified',
            xaxis={'tickangle': -45}
        )
        
        return fig
    except:
        return None

def categorize_rsrp_4g(value):
    """Kategorisasi RSRP 4G"""
    if pd.isna(value):
        return "No Data"
    elif value >= -80:
        return "Excellent"
    elif value >= -90:
        return "Good"
    elif value >= -100:
        return "Fair"
    else:
        return "Poor"

# ===== MAIN APP =====

def main():
    # Header
    st.markdown('<p class="main-header">📡 Dashboard QoS Telekomunikasi</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Analisis Kualitas Layanan: Indosat, Telkomsel, XL</p>', unsafe_allow_html=True)
    
    # Sidebar - Data Source
    st.sidebar.title("📁 Sumber Data")
    
    # Scan folder data
    data_files = get_data_files(DATA_FOLDER)
    
    # Source selection
    data_source = st.sidebar.radio(
        "Pilih Sumber Data",
        ["📂 Dari Folder 'data'", "📤 Upload Manual"],
        help="Pilih dari folder 'data' atau upload file baru"
    )
    
    file_path = None
    
    if data_source == "📂 Dari Folder 'data'":
        if not data_files:
            st.sidebar.warning("⚠️ Tidak ada file di folder 'data'")
            st.info(f"""
            📁 **Cara menggunakan:**
            1. Buat folder bernama `data` di direktori yang sama dengan `qos_dashboard.py`
            2. Letakkan file Excel (.xlsx, .xls) atau CSV (.csv) di folder tersebut
            3. Refresh halaman ini
            
            **Folder path:** `{os.path.abspath(DATA_FOLDER)}`
            """)
            return
        
        # Dropdown file selection
        file_names = [os.path.basename(f) for f in data_files]
        selected_file_name = st.sidebar.selectbox(
            "Pilih File",
            file_names,
            help="File diurutkan berdasarkan waktu modifikasi (terbaru di atas)"
        )
        
        # Get selected file path
        selected_idx = file_names.index(selected_file_name)
        file_path = data_files[selected_idx]
        
        # Display file info
        file_info = get_file_info(file_path)
        if file_info:
            st.sidebar.markdown(f"""
            <div class="file-info">
            <strong>📄 File Info:</strong><br>
            📝 Nama: {file_info['name']}<br>
            📊 Ukuran: {file_info['size']}<br>
            🕐 Modified: {file_info['modified']}
            </div>
            """, unsafe_allow_html=True)
    
    else:  # Upload Manual
        uploaded_file = st.sidebar.file_uploader(
            "Upload File Data",
            type=['xlsx', 'xls', 'csv'],
            help="Format: Excel (.xlsx, .xls) atau CSV (.csv)"
        )
        
        if uploaded_file is None:
            st.sidebar.info("👆 Silakan upload file data")
            st.info("""
            📤 **Upload File:**
            1. Klik tombol "Browse files" di sidebar
            2. Pilih file Excel atau CSV Anda
            3. Dashboard akan otomatis memuat data
            
            **Format yang didukung:** .xlsx, .xls, .csv
            """)
            return
        else:
            file_path = uploaded_file
            st.sidebar.success(f"✅ File uploaded: {uploaded_file.name}")
    
    # Load data
    if file_path is None:
        st.warning("⚠️ Tidak ada file yang dipilih")
        return
    
    with st.spinner('⏳ Memuat dan memproses data...'):
        df, error = load_and_prepare_data(file_path)
    
    if error:
        st.error(f"❌ {error}")
        return
    
    if df is None or len(df) == 0:
        st.error("❌ Tidak ada data yang bisa dimuat")
        return
    
    st.sidebar.success(f"✅ Data loaded: {len(df):,} baris")
    
    # Sidebar Filters
    st.sidebar.markdown("---")
    st.sidebar.title("🔍 Filter Data")
    
    # Filter Kabupaten/Kota
    kabkota_options = ['Semua'] + sorted([str(k) for k in df['Kabupaten / Kota'].unique() if pd.notna(k)])
    selected_kabkota = st.sidebar.selectbox("Kabupaten/Kota", kabkota_options)
    
    df_filtered = df.copy()
    if selected_kabkota != 'Semua':
        df_filtered = df_filtered[df_filtered['Kabupaten / Kota'] == selected_kabkota]
    
    # Filter Lokasi
    lokasi_options = ['Semua'] + sorted([str(l) for l in df_filtered['Lokasi Pengukuran'].unique() if pd.notna(l)])
    selected_lokasi = st.sidebar.selectbox("Lokasi Pengukuran", lokasi_options)
    
    if selected_lokasi != 'Semua':
        df_filtered = df_filtered[df_filtered['Lokasi Pengukuran'] == selected_lokasi]
    
    # Filter Operator
    operator_options = ['Semua'] + sorted(ALLOWED_OPERATORS)
    selected_operators = st.sidebar.multiselect(
        "Operator",
        operator_options,
        default='Semua'
    )
    
    if 'Semua' not in selected_operators and selected_operators:
        df_filtered = df_filtered[df_filtered['Operator'].isin(selected_operators)]
    
    # Display metrics
    st.sidebar.markdown("---")
    st.sidebar.metric("📊 Total Data", f"{len(df_filtered):,}")
    st.sidebar.metric("📍 Lokasi Unik", df_filtered['Lokasi Pengukuran'].nunique())
    st.sidebar.metric("🏢 Operator", df_filtered['Operator'].nunique())
    
    if df_filtered.empty:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter")
        st.info("💡 Coba reset filter dengan memilih 'Semua'")
        return
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Overview",
        "📡 Signal Quality",
        "🚀 Speed Test",
        "📹 YouTube & Ping",
        "🔄 Comparison 4G vs 2G",
        "📍 Per Lokasi",
        "📋 Kesimpulan"
    ])
    
    # ===== TAB 1: OVERVIEW =====
    with tab1:
        st.markdown("### 📊 Overview Data QoS")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Total Pengukuran", f"{len(df_filtered):,}")
        
        with col2:
            st.metric("📍 Lokasi", df_filtered['Lokasi Pengukuran'].nunique())
        
        with col3:
            st.metric("🏢 Operator", df_filtered['Operator'].nunique())
        
        with col4:
            if 'Average Speed Test DL (Mbps) (4G)' in df_filtered.columns:
                avg_speed = safe_agg(df_filtered['Average Speed Test DL (Mbps) (4G)'])
                st.metric("⚡ Avg DL 4G", f"{avg_speed:.2f} Mbps" if pd.notna(avg_speed) else "N/A")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            op_counts = df_filtered['Operator'].value_counts()
            fig = px.pie(
                values=op_counts.values,
                names=op_counts.index,
                title="Distribusi Pengukuran per Operator",
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
                title="Top 10 Lokasi Pengukuran",
                labels={'x': 'Jumlah', 'y': 'Lokasi'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.markdown("### 📈 Statistik Ringkas per Operator")
        
        summary_metrics = {}
        metric_cols = {
            'RSRP 4G (dBm)': 'Average RSRP (Signal Strenght 4G)',
            'DL Speed 4G (Mbps)': 'Average Speed Test DL (Mbps) (4G)',
            'YouTube SR (%)': 'Youtube SR (%)',
            'Latency (ms)': 'Average RTT Latency (ms)'
        }
        
        for label, col in metric_cols.items():
            if col in df_filtered.columns:
                summary_metrics[label] = {
                    'Indosat': safe_agg(df_filtered[df_filtered['Operator']=='Indosat'][col]),
                    'Telkomsel': safe_agg(df_filtered[df_filtered['Operator']=='Telkomsel'][col]),
                    'XL': safe_agg(df_filtered[df_filtered['Operator']=='XL'][col])
                }
        
        if summary_metrics:
            summary_df = pd.DataFrame(summary_metrics).T
            summary_df = summary_df.round(2)
            st.dataframe(summary_df, use_container_width=True)
    
    # ===== TAB 2: SIGNAL QUALITY =====
    with tab2:
        st.markdown("### 📡 Signal Quality Analysis")
        
        tech_select = st.radio("Pilih Teknologi", ["4G", "2G"], horizontal=True)
        
        if tech_select == "4G":
            st.markdown("#### 📡 RSRP 4G")
            
            if 'Average RSRP (Signal Strenght 4G)' in df_filtered.columns:
                agg_data = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average RSRP (Signal Strenght 4G)': lambda x: safe_agg(x)
                })
                
                fig = create_bar_chart(
                    agg_data,
                    'Lokasi Pengukuran',
                    'Average RSRP (Signal Strenght 4G)',
                    'RSRP 4G per Operator dan Lokasi'
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Data RSRP 4G tidak tersedia")
            
            st.markdown("#### 📊 RSRQ 4G")
            
            if 'Average RSRQ (Signal Qualty 4G)' in df_filtered.columns:
                agg_data = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average RSRQ (Signal Qualty 4G)': lambda x: safe_agg(x)
                })
                
                fig = create_bar_chart(
                    agg_data,
                    'Lokasi Pengukuran',
                    'Average RSRQ (Signal Qualty 4G)',
                    'RSRQ 4G per Operator dan Lokasi'
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### 📈 SINR 4G")
            
            if 'Average SINR (Signal Qualty 4G)' in df_filtered.columns:
                agg_data = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average SINR (Signal Qualty 4G)': lambda x: safe_agg(x)
                })
                
                fig = create_bar_chart(
                    agg_data,
                    'Lokasi Pengukuran',
                    'Average SINR (Signal Qualty 4G)',
                    'SINR 4G per Operator dan Lokasi'
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Summary
            st.markdown("#### 📋 Summary Signal 4G")
            summary_cols = [
                'Average RSRP (Signal Strenght 4G)',
                'Average RSRQ (Signal Qualty 4G)',
                'Average SINR (Signal Qualty 4G)'
            ]
            available = [c for c in summary_cols if c in df_filtered.columns]
            
            if available:
                summary = df_filtered.groupby('Operator')[available].agg(
                    lambda x: safe_agg(x)
                ).round(2)
                st.dataframe(summary, use_container_width=True)
        
        else:  # 2G
            st.markdown("#### 📡 RxLevel 2G")
            
            if 'Average RX Level (Signal Strenght 2G)' in df_filtered.columns:
                agg_data = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average RX Level (Signal Strenght 2G)': lambda x: safe_agg(x)
                })
                
                fig = create_bar_chart(
                    agg_data,
                    'Lokasi Pengukuran',
                    'Average RX Level (Signal Strenght 2G)',
                    'RxLevel 2G per Operator dan Lokasi'
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### 📊 RxQual 2G")
            
            if 'Average RX Qual (Signal Quality 2G)' in df_filtered.columns:
                agg_data = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average RX Qual (Signal Quality 2G)': lambda x: safe_agg(x)
                })
                
                fig = create_bar_chart(
                    agg_data,
                    'Lokasi Pengukuran',
                    'Average RX Qual (Signal Quality 2G)',
                    'RxQual 2G per Operator dan Lokasi'
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    # ===== TAB 3: SPEED TEST =====
    with tab3:
        st.markdown("### 🚀 Speed Test Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 Download Speed 4G")
            
            if 'Average Speed Test DL (Mbps) (4G)' in df_filtered.columns:
                agg_data = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average Speed Test DL (Mbps) (4G)': lambda x: safe_agg(x)
                })
                
                fig = create_bar_chart(
                    agg_data,
                    'Lokasi Pengukuran',
                    'Average Speed Test DL (Mbps) (4G)',
                    'Download Speed 4G'
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📤 Upload Speed 4G")
            
            if 'Average Speed Test UL (Mbps) (4G)' in df_filtered.columns:
                agg_data = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average Speed Test UL (Mbps) (4G)': lambda x: safe_agg(x)
                })
                
                fig = create_bar_chart(
                    agg_data,
                    'Lokasi Pengukuran',
                    'Average Speed Test UL (Mbps) (4G)',
                    'Upload Speed 4G'
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌐 Browsing Success Rate")
            
            if 'Browsing Success (%)' in df_filtered.columns:
                agg_data = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Browsing Success (%)': lambda x: safe_agg(x)
                })
                
                fig = create_bar_chart(
                    agg_data,
                    'Lokasi Pengukuran',
                    'Browsing Success (%)',
                    'Browsing Success Rate'
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### ⚡ Browsing Speed")
            
            if 'Average Browsing Speed (Mbps)' in df_filtered.columns:
                agg_data = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average Browsing Speed (Mbps)': lambda x: safe_agg(x)
                })
                
                fig = create_bar_chart(
                    agg_data,
                    'Lokasi Pengukuran',
                    'Average Browsing Speed (Mbps)',
                    'Browsing Speed'
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    # ===== TAB 4: YOUTUBE & PING =====
    with tab4:
        st.markdown("### 📹 YouTube & Ping Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📹 YouTube Success Rate")
            
            if 'Youtube SR (%)' in df_filtered.columns:
                agg_data = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Youtube SR (%)': lambda x: safe_agg(x)
                })
                
                fig = create_bar_chart(
                    agg_data,
                    'Lokasi Pengukuran',
                    'Youtube SR (%)',
                    'YouTube Success Rate'
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🏓 Ping Latency")
            
            if 'Average RTT Latency (ms)' in df_filtered.columns:
                agg_data = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average RTT Latency (ms)': lambda x: safe_agg(x)
                })
                
                fig = create_bar_chart(
                    agg_data,
                    'Lokasi Pengukuran',
                    'Average RTT Latency (ms)',
                    'Ping Latency (Lower is Better)'
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    # ===== TAB 5: 4G vs 2G =====
    with tab5:
        st.markdown("### 🔄 Comparison 4G vs 2G")
        
        operators = sorted(df_filtered['Operator'].unique())
        if operators:
            selected_op = st.selectbox("Pilih Operator", operators)
            
            df_op = df_filtered[df_filtered['Operator'] == selected_op]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📡 Signal Strength")
                
                has_4g = 'Average RSRP (Signal Strenght 4G)' in df_op.columns
                has_2g = 'Average RX Level (Signal Strenght 2G)' in df_op.columns
                
                if has_4g or has_2g:
                    agg_dict = {}
                    if has_4g:
                        agg_dict['4G_RSRP'] = pd.NamedAgg(
                            column='Average RSRP (Signal Strenght 4G)',
                            aggfunc=lambda x: safe_agg(x)
                        )
                    if has_2g:
                        agg_dict['2G_RxLevel'] = pd.NamedAgg(
                            column='Average RX Level (Signal Strenght 2G)',
                            aggfunc=lambda x: safe_agg(x)
                        )
                    
                    signal_comp = df_op.groupby('Lokasi Pengukuran', as_index=False).agg(**agg_dict)
                    
                    fig = go.Figure()
                    
                    if has_4g:
                        fig.add_trace(go.Bar(
                            name='4G RSRP',
                            x=signal_comp['Lokasi Pengukuran'],
                            y=signal_comp['4G_RSRP'],
                            marker_color='#4169E1'
                        ))
                    
                    if has_2g:
                        fig.add_trace(go.Bar(
                            name='2G RxLevel',
                            x=signal_comp['Lokasi Pengukuran'],
                            y=signal_comp['2G_RxLevel'],
                            marker_color='#FF6347'
                        ))
                    
                    fig.update_layout(
                        title=f'Signal: 4G vs 2G - {selected_op}',
                        xaxis_title='Lokasi',
                        yaxis_title='Signal (dBm)',
                        barmode='group',
                        height=500,
                        xaxis={'tickangle': -45}
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 🚀 Speed")
                
                has_4g_speed = 'Average Speed Test DL (Mbps) (4G)' in df_op.columns
                has_2g_speed = 'Average Speed Test DL (Mbps) (2G)' in df_op.columns
                
                if has_4g_speed or has_2g_speed:
                    agg_dict = {}
                    if has_4g_speed:
                        agg_dict['4G_DL'] = pd.NamedAgg(
                            column='Average Speed Test DL (Mbps) (4G)',
                            aggfunc=lambda x: safe_agg(x)
                        )
                    if has_2g_speed:
                        agg_dict['2G_DL'] = pd.NamedAgg(
                            column='Average Speed Test DL (Mbps) (2G)',
                            aggfunc=lambda x: safe_agg(x)
                        )
                    
                    speed_comp = df_op.groupby('Lokasi Pengukuran', as_index=False).agg(**agg_dict)
                    
                    fig = go.Figure()
                    
                    if has_4g_speed:
                        fig.add_trace(go.Bar(
                            name='4G Download',
                            x=speed_comp['Lokasi Pengukuran'],
                            y=speed_comp['4G_DL'],
                            marker_color='#32CD32'
                        ))
                    
                    if has_2g_speed:
                        fig.add_trace(go.Bar(
                            name='2G Download',
                            x=speed_comp['Lokasi Pengukuran'],
                            y=speed_comp['2G_DL'],
                            marker_color='#FFD700'
                        ))
                    
                    fig.update_layout(
                        title=f'Speed: 4G vs 2G - {selected_op}',
                        xaxis_title='Lokasi',
                        yaxis_title='Speed (Mbps)',
                        barmode='group',
                        height=500,
                        xaxis={'tickangle': -45}
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
    
    # ===== TAB 6: PER LOKASI =====
    with tab6:
        st.markdown("### 📍 Analisis per Lokasi")
        
        locations = sorted(df_filtered['Lokasi Pengukuran'].unique())
        if locations:
            selected_loc = st.selectbox("Pilih Lokasi", locations)
            
            df_loc = df_filtered[df_filtered['Lokasi Pengukuran'] == selected_loc]
            
            st.markdown(f"#### 📍 {selected_loc}")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Operator", df_loc['Operator'].nunique())
            
            with col2:
                if 'Average RSRP (Signal Strenght 4G)' in df_loc.columns:
                    avg = safe_agg(df_loc['Average RSRP (Signal Strenght 4G)'])
                    st.metric("Avg RSRP 4G", f"{avg:.2f} dBm" if pd.notna(avg) else "N/A")
            
            with col3:
                if 'Average Speed Test DL (Mbps) (4G)' in df_loc.columns:
                    avg = safe_agg(df_loc['Average Speed Test DL (Mbps) (4G)'])
                    st.metric("Avg DL 4G", f"{avg:.2f} Mbps" if pd.notna(avg) else "N/A")
            
            with col4:
                if 'Youtube SR (%)' in df_loc.columns:
                    avg = safe_agg(df_loc['Youtube SR (%)'])
                    st.metric("YouTube SR", f"{avg:.1f}%" if pd.notna(avg) else "N/A")
            
            st.markdown("---")
            
            # Radar chart
            st.markdown("#### 🎯 Multi-Dimension Comparison")
            
            radar_metrics = {
                'Signal 4G': 'Average RSRP (Signal Strenght 4G)',
                'Quality 4G': 'Average RSRQ (Signal Qualty 4G)',
                'DL Speed': 'Average Speed Test DL (Mbps) (4G)',
                'UL Speed': 'Average Speed Test UL (Mbps) (4G)',
                'YouTube SR': 'Youtube SR (%)'
            }
            
            available_radar = {k: v for k, v in radar_metrics.items() if v in df_loc.columns}
            
            if available_radar:
                fig = go.Figure()
                
                for operator in df_loc['Operator'].unique():
                    df_op = df_loc[df_loc['Operator'] == operator]
                    
                    values = []
                    for metric in available_radar.values():
                        val = safe_agg(df_op[metric])
                        values.append(val if pd.notna(val) else 0)
                    
                    if values and any(v != 0 for v in values):
                        values.append(values[0])
                        
                        fig.add_trace(go.Scatterpolar(
                            r=values,
                            theta=list(available_radar.keys()) + [list(available_radar.keys())[0]],
                            fill='toself',
                            name=operator
                        ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True)),
                    showlegend=True,
                    title=f"Radar Chart - {selected_loc}",
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Detail table
            st.markdown("#### 📊 Detail Metrics per Operator")
            
            detail_cols = [
                'Average RSRP (Signal Strenght 4G)',
                'Average RSRQ (Signal Qualty 4G)',
                'Average Speed Test DL (Mbps) (4G)',
                'Average Speed Test UL (Mbps) (4G)',
                'Youtube SR (%)',
                'Average RTT Latency (ms)'
            ]
            
            available_detail = [c for c in detail_cols if c in df_loc.columns]
            
            if available_detail:
                detail = df_loc.groupby('Operator')[available_detail].agg(
                    lambda x: safe_agg(x)
                ).round(2)
                st.dataframe(detail, use_container_width=True)
    
    # ===== TAB 7: KESIMPULAN =====
    with tab7:
        st.markdown("### 📋 Kesimpulan Analisis QoS")
        
        region_options = ['Semua Lokasi'] + sorted(df['Kabupaten / Kota'].unique().tolist())
        region = st.selectbox("Pilih Wilayah", region_options)
        
        if region == 'Semua Lokasi':
            df_conc = df_filtered
            region_title = "Semua Lokasi (Terfilter)"
        else:
            df_conc = df[df['Kabupaten / Kota'] == region]
            region_title = region
        
        st.markdown(f"#### 📍 {region_title}")
        
        if df_conc.empty:
            st.warning("Tidak ada data")
        else:
            locations = sorted(df_conc['Lokasi Pengukuran'].unique())
            
            for idx, loc in enumerate(locations[:5], 1):
                with st.expander(f"📌 {loc}", expanded=(idx == 1)):
                    loc_data = df_conc[df_conc['Lokasi Pengukuran'] == loc]
                    
                    for operator in sorted(loc_data['Operator'].unique()):
                        op_data = loc_data[loc_data['Operator'] == operator]
                        
                        st.markdown(f"**{operator}:**")
                        
                        if 'Average RSRP (Signal Strenght 4G)' in op_data.columns:
                            rsrp = safe_agg(op_data['Average RSRP (Signal Strenght 4G)'])
                            if pd.notna(rsrp):
                                cat = categorize_rsrp_4g(rsrp)
                                st.write(f"- 4G Signal: {cat} (RSRP: {rsrp:.2f} dBm)")
                        
                        if 'Average Speed Test DL (Mbps) (4G)' in op_data.columns:
                            dl = safe_agg(op_data['Average Speed Test DL (Mbps) (4G)'])
                            if pd.notna(dl):
                                st.write(f"- Download 4G: {dl:.2f} Mbps")
                        
                        if 'Youtube SR (%)' in op_data.columns:
                            yt = safe_agg(op_data['Youtube SR (%)'])
                            if pd.notna(yt):
                                status = "Baik" if yt >= 95 else "Cukup" if yt >= 85 else "Kurang"
                                st.write(f"- YouTube: {status} ({yt:.1f}%)")
                        
                        st.markdown("")
                    
                    # Ranking
                    st.markdown("**🏆 Ranking (Download Speed 4G):**")
                    
                    if 'Average Speed Test DL (Mbps) (4G)' in loc_data.columns:
                        ranking_data = []
                        for op in loc_data['Operator'].unique():
                            speed = safe_agg(loc_data[loc_data['Operator']==op]['Average Speed Test DL (Mbps) (4G)'])
                            if pd.notna(speed):
                                ranking_data.append({'Operator': op, 'Speed': speed})
                        
                        if ranking_data:
                            ranking_df = pd.DataFrame(ranking_data).sort_values('Speed', ascending=False)
                            
                            for rank, row in enumerate(ranking_df.itertuples(), 1):
                                medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
                                st.write(f"{medal} {rank}. {row.Operator}: {row.Speed:.2f} Mbps")
            
            if len(locations) > 5:
                st.info(f"Menampilkan 5 dari {len(locations)} lokasi")
            
            st.markdown("---")
            
            # Overall summary
            st.markdown("### 📊 Summary Keseluruhan")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏆 Best Performers")
                
                if 'Average RSRP (Signal Strenght 4G)' in df_conc.columns:
                    best_data = []
                    for op in ALLOWED_OPERATORS:
                        val = safe_agg(df_conc[df_conc['Operator']==op]['Average RSRP (Signal Strenght 4G)'])
                        if pd.notna(val):
                            best_data.append({'Operator': op, 'Value': val})
                    
                    if best_data:
                        best_df = pd.DataFrame(best_data).sort_values('Value', ascending=False)
                        best_op = best_df.iloc[0]
                        st.write(f"**Best Signal 4G:** {best_op['Operator']} ({best_op['Value']:.2f} dBm)")
                
                if 'Average Speed Test DL (Mbps) (4G)' in df_conc.columns:
                    best_data = []
                    for op in ALLOWED_OPERATORS:
                        val = safe_agg(df_conc[df_conc['Operator']==op]['Average Speed Test DL (Mbps) (4G)'])
                        if pd.notna(val):
                            best_data.append({'Operator': op, 'Value': val})
                    
                    if best_data:
                        best_df = pd.DataFrame(best_data).sort_values('Value', ascending=False)
                        best_op = best_df.iloc[0]
                        st.write(f"**Best DL Speed:** {best_op['Operator']} ({best_op['Value']:.2f} Mbps)")
            
            with col2:
                st.markdown("#### 📉 Latency")
                
                if 'Average RTT Latency (ms)' in df_conc.columns:
                    lat_data = []
                    for op in ALLOWED_OPERATORS:
                        val = safe_agg(df_conc[df_conc['Operator']==op]['Average RTT Latency (ms)'])
                        if pd.notna(val):
                            lat_data.append({'Operator': op, 'Value': val})
                    
                    if lat_data:
                        lat_df = pd.DataFrame(lat_data).sort_values('Value')
                        best_lat = lat_df.iloc[0]
                        worst_lat = lat_df.iloc[-1]
                        
                        st.write(f"**Best (Lowest):** {best_lat['Operator']} ({best_lat['Value']:.2f} ms)")
                        st.write(f"**Worst (Highest):** {worst_lat['Operator']} ({worst_lat['Value']:.2f} ms)")
            
            # Overall table
            st.markdown("#### 📊 Overall Performance Table")
            
            overall_cols = [
                'Average RSRP (Signal Strenght 4G)',
                'Average Speed Test DL (Mbps) (4G)',
                'Average Speed Test UL (Mbps) (4G)',
                'Youtube SR (%)',
                'Average RTT Latency (ms)'
            ]
            
            available_overall = [c for c in overall_cols if c in df_conc.columns]
            
            if available_overall:
                overall = df_conc.groupby('Operator')[available_overall].agg(
                    lambda x: safe_agg(x)
                ).round(2)
                
                col_rename = {
                    'Average RSRP (Signal Strenght 4G)': 'RSRP (dBm)',
                    'Average Speed Test DL (Mbps) (4G)': 'DL (Mbps)',
                    'Average Speed Test UL (Mbps) (4G)': 'UL (Mbps)',
                    'Youtube SR (%)': 'YouTube (%)',
                    'Average RTT Latency (ms)': 'Latency (ms)'
                }
                
                overall.columns = [col_rename.get(c, c) for c in overall.columns]
                
                if 'DL (Mbps)' in overall.columns:
                    overall = overall.sort_values('DL (Mbps)', ascending=False)
                
                st.dataframe(overall, use_container_width=True)

if __name__ == "__main__":
    main()