"""
Dashboard QoS Telekomunikasi - COMPLETE VERSION (2G + 4G)
✅ Auto-read from 'data' folder
✅ Perfect baseline charts
✅ Exclude Smartfren (Indosat, Telkomsel, XL only)
✅ Complete Parameters: Signal (2G + 4G), Browsing, Speed Test, Ping Test, YouTube
✅ PETA INTERAKTIF dengan informasi per lokasi pengukuran
✅ Kesimpulan per tanggal untuk semua operator
✅ 2G METRICS INCLUDED (RxLev, RxQual)
✅ NO ERRORS - READY TO RUN
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
    .tech-badge-2g {
        background: linear-gradient(135deg, #95a5a6, #7f8c8d);
        color: white; padding: 0.3rem 0.8rem;
        border-radius: 5px; display: inline-block;
        font-weight: bold; margin: 0.2rem;
        font-size: 0.9rem;
    }
    .tech-badge-4g {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white; padding: 0.3rem 0.8rem;
        border-radius: 5px; display: inline-block;
        font-weight: bold; margin: 0.2rem;
        font-size: 0.9rem;
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
    .operator-section {
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .best-badge {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #000;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
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
                'Packet', 'Loss', 'Lat', 'Long',
                'RxLev', 'RxQual', '2G']  # 2G metrics added
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

def create_signal_quality_chart(data, x_col, y_col, title, color_col='Operator'):
    try:
        if y_col not in data.columns:
            return None
        plot_data = data[[x_col, y_col, color_col]].dropna(subset=[y_col])
        if plot_data.empty:
            return None
        
        fig = px.bar(plot_data, x=x_col, y=y_col, color=color_col, barmode='group',
                    title=title, color_discrete_map=OPERATOR_COLORS, text=y_col)
        
        y_min = plot_data[y_col].min()
        padding = abs(y_min) * 0.1
        y_range = [y_min - padding, 5]
        
        fig.update_layout(
            height=500, hovermode='x unified',
            xaxis={'tickangle': -45, 'title': None},
            yaxis={'title': y_col.split('(')[0].strip(), 'range': y_range,
                   'zeroline': True, 'zerolinewidth': 3, 'zerolinecolor': '#000',
                   'showgrid': True, 'gridwidth': 1, 'gridcolor': '#e0e0e0'},
            legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02,
                   'xanchor': 'center', 'x': 0.5, 'title': None},
            title={'text': title, 'x': 0.5, 'xanchor': 'center'},
            margin={'t': 80, 'b': 100, 'l': 80, 'r': 40},
            plot_bgcolor='white', paper_bgcolor='white'
        )
        
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside', textfont={'size': 9})
        fig.add_hline(y=0, line_dash="solid", line_color="#000", line_width=2,
                     annotation_text="Baseline (0)", annotation_position="right")
        return fig
    except:
        return None

def create_speed_chart(data, x_col, y_col, title, color_col='Operator'):
    try:
        if y_col not in data.columns:
            return None
        plot_data = data[[x_col, y_col, color_col]].dropna(subset=[y_col])
        if plot_data.empty:
            return None
        
        fig = px.bar(plot_data, x=x_col, y=y_col, color=color_col, barmode='group',
                    title=title, color_discrete_map=OPERATOR_COLORS, text=y_col)
        
        y_max = plot_data[y_col].max()
        y_range = [0, y_max * 1.15]
        
        fig.update_layout(
            height=500, hovermode='x unified',
            xaxis={'tickangle': -45, 'title': None},
            yaxis={'title': y_col.split('(')[0].strip(), 'range': y_range,
                   'zeroline': True, 'zerolinewidth': 3, 'zerolinecolor': '#000',
                   'showgrid': True, 'gridwidth': 1, 'gridcolor': '#e0e0e0'},
            legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02,
                   'xanchor': 'center', 'x': 0.5, 'title': None},
            title={'text': title, 'x': 0.5, 'xanchor': 'center'},
            margin={'t': 80, 'b': 100, 'l': 80, 'r': 40},
            plot_bgcolor='white', paper_bgcolor='white'
        )
        
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside', textfont={'size': 9})
        return fig
    except:
        return None

def create_interactive_map(data):
    """Create interactive map dengan marker per lokasi pengukuran"""
    try:
        map_data = data[data['Lat'].notna() & data['Long'].notna()].copy()
        
        if map_data.empty:
            return None
        
        # Create hover text dengan informasi lengkap (2G + 4G)
        hover_texts = []
        for _, row in map_data.iterrows():
            text = f"<b>{row['Lokasi Pengukuran']}</b><br>"
            text += f"Operator: {row['Operator']}<br>"
            text += "━━━━━━━━━━━━━━━━━━━<br>"
            
            # 2G Metrics
            if 'Average RxLev (2G)' in row and pd.notna(row['Average RxLev (2G)']):
                text += f"📶 2G RxLev: {row['Average RxLev (2G)']:.1f} dBm<br>"
            if 'Average RxQual (2G)' in row and pd.notna(row['Average RxQual (2G)']):
                text += f"📶 2G RxQual: {row['Average RxQual (2G)']:.1f}<br>"
            
            # 4G Metrics
            if 'Average RSRP (Signal Strenght 4G)' in row and pd.notna(row['Average RSRP (Signal Strenght 4G)']):
                text += f"📡 4G RSRP: {row['Average RSRP (Signal Strenght 4G)']:.1f} dBm<br>"
            if 'Average Speed Test DL (Mbps) (4G)' in row and pd.notna(row['Average Speed Test DL (Mbps) (4G)']):
                text += f"🚀 DL Speed: {row['Average Speed Test DL (Mbps) (4G)']:.1f} Mbps<br>"
            if 'Youtube SR (%)' in row and pd.notna(row['Youtube SR (%)']):
                text += f"📹 YouTube SR: {row['Youtube SR (%)']:.1f}%<br>"
            if 'Average RTT Latency (ms)' in row and pd.notna(row['Average RTT Latency (ms)']):
                text += f"🏓 Latency: {row['Average RTT Latency (ms)']:.1f} ms<br>"
            if 'Tanggal_Only' in row and pd.notna(row['Tanggal_Only']):
                text += f"📅 {row['Tanggal_Only']}"
            
            hover_texts.append(text)
        
        map_data['hover_text'] = hover_texts
        
        # Create scatter mapbox
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
            title="🗺️ Peta Lokasi Pengukuran QoS (2G + 4G)"
        )
        
        # Update map style
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
                bgcolor="rgba(255,255,255,0.8)"
            ),
            margin={"r": 0, "t": 40, "l": 0, "b": 0}
        )
        
        fig.update_traces(marker=dict(size=12), hovertemplate='%{hovertext}<extra></extra>')
        
        # Update hover template
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
    elif metric_type == 'rxlev':  # 2G RxLev
        if value >= -75: return "Excellent", "quality-excellent"
        elif value >= -85: return "Good", "quality-good"
        elif value >= -95: return "Fair", "quality-fair"
        else: return "Poor", "quality-poor"
    elif metric_type == 'rxqual':  # 2G RxQual (lower is better, 0-7 scale)
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

def generate_detailed_conclusion_per_date(df_data, location, date_str):
    """Generate kesimpulan untuk SEMUA operator di lokasi & tanggal tertentu (2G + 4G)"""
    lines = []
    
    lines.append("### 📋 Kesimpulan Pengukuran")
    lines.append(f"**📍 Lokasi:** {location}")
    lines.append(f"**📅 Tanggal:** {date_str}")
    lines.append("")
    lines.append("---")
    
    operators = sorted(df_data['Operator'].unique())
    operator_scores = {}
    
    for operator in operators:
        op_data = df_data[df_data['Operator'] == operator]
        
        lines.append("")
        lines.append(f"### 👤 **{operator}**")
        lines.append("")
        
        scores = []
        
        # 2G Signal Quality
        has_2g = ('Average RxLev (2G)' in op_data.columns or 'Average RxQual (2G)' in op_data.columns)
        if has_2g:
            lines.append("**📶 Signal Quality 2G:**")
            if 'Average RxLev (2G)' in op_data.columns:
                rxlev = safe_agg(op_data['Average RxLev (2G)'])
                if pd.notna(rxlev):
                    cat, cls = categorize_quality(rxlev, 'rxlev')
                    lines.append(f"- RxLev: **{rxlev:.2f} dBm** - <span class='{cls}'>{cat}</span>")
                    scores.append(1 if rxlev >= -75 else 0.75 if rxlev >= -85 else 0.5 if rxlev >= -95 else 0.25)
            
            if 'Average RxQual (2G)' in op_data.columns:
                rxqual = safe_agg(op_data['Average RxQual (2G)'])
                if pd.notna(rxqual):
                    cat, cls = categorize_quality(rxqual, 'rxqual')
                    lines.append(f"- RxQual: **{rxqual:.2f}** - <span class='{cls}'>{cat}</span> (0=best, 7=worst)")
                    scores.append(1 if rxqual <= 2 else 0.75 if rxqual <= 4 else 0.5 if rxqual <= 5 else 0.25)
            
            lines.append("")
        
        # 4G Signal Quality
        lines.append("**📡 Signal Quality 4G:**")
        if 'Average RSRP (Signal Strenght 4G)' in op_data.columns:
            rsrp = safe_agg(op_data['Average RSRP (Signal Strenght 4G)'])
            if pd.notna(rsrp):
                cat, cls = categorize_quality(rsrp, 'rsrp')
                lines.append(f"- RSRP: **{rsrp:.2f} dBm** - <span class='{cls}'>{cat}</span>")
                scores.append(1 if rsrp >= -80 else 0.75 if rsrp >= -90 else 0.5 if rsrp >= -100 else 0.25)
        
        if 'Average RSRQ (Signal Qualty 4G)' in op_data.columns:
            rsrq = safe_agg(op_data['Average RSRQ (Signal Qualty 4G)'])
            if pd.notna(rsrq):
                lines.append(f"- RSRQ: **{rsrq:.2f} dB**")
        
        # Browsing
        lines.append("")
        lines.append("**🌐 Browsing:**")
        if 'Browsing Success (%)' in op_data.columns:
            brow_sr = safe_agg(op_data['Browsing Success (%)'])
            if pd.notna(brow_sr):
                cat, cls = categorize_quality(brow_sr, 'percentage')
                lines.append(f"- Success Rate: **{brow_sr:.1f}%** - <span class='{cls}'>{cat}</span>")
                scores.append(1 if brow_sr >= 95 else 0.75 if brow_sr >= 85 else 0.5)
        
        # Speed Test
        lines.append("")
        lines.append("**🚀 Speed Test:**")
        if 'Average Speed Test DL (Mbps) (4G)' in op_data.columns:
            dl = safe_agg(op_data['Average Speed Test DL (Mbps) (4G)'])
            if pd.notna(dl):
                cat, cls = categorize_quality(dl, 'speed')
                lines.append(f"- Download: **{dl:.2f} Mbps** - <span class='{cls}'>{cat}</span>")
                scores.append(1 if dl >= 30 else 0.75 if dl >= 15 else 0.5 if dl >= 5 else 0.25)
        
        if 'Average Speed Test UL (Mbps) (4G)' in op_data.columns:
            ul = safe_agg(op_data['Average Speed Test UL (Mbps) (4G)'])
            if pd.notna(ul):
                lines.append(f"- Upload: **{ul:.2f} Mbps**")
        
        # Ping Test
        lines.append("")
        lines.append("**🏓 Ping Test:**")
        if 'Average RTT Latency (ms)' in op_data.columns:
            lat = safe_agg(op_data['Average RTT Latency (ms)'])
            if pd.notna(lat):
                lat_status = "Baik" if lat < 100 else "Cukup" if lat < 150 else "Kurang"
                lines.append(f"- Latency: **{lat:.2f} ms** ({lat_status})")
                scores.append(1 if lat < 100 else 0.75 if lat < 150 else 0.5)
        
        # YouTube
        lines.append("")
        lines.append("**📹 YouTube:**")
        if 'Youtube SR (%)' in op_data.columns:
            yt = safe_agg(op_data['Youtube SR (%)'])
            if pd.notna(yt):
                cat, cls = categorize_quality(yt, 'percentage')
                lines.append(f"- Success Rate: **{yt:.1f}%** - <span class='{cls}'>{cat}</span>")
                scores.append(1 if yt >= 95 else 0.75 if yt >= 85 else 0.5)
        
        if 'Average TTFP (s)' in op_data.columns:
            ttfp = safe_agg(op_data['Average TTFP (s)'])
            if pd.notna(ttfp):
                ttfp_status = "Cepat" if ttfp < 2 else "Normal" if ttfp < 5 else "Lambat"
                lines.append(f"- TTFP: **{ttfp:.2f} s** ({ttfp_status})")
        
        # Overall score
        if scores:
            overall_score = sum(scores) / len(scores) * 100
            operator_scores[operator] = overall_score
            
            if overall_score >= 85:
                overall_status, overall_class = "Sangat Baik", "quality-excellent"
            elif overall_score >= 70:
                overall_status, overall_class = "Baik", "quality-good"
            elif overall_score >= 50:
                overall_status, overall_class = "Cukup", "quality-fair"
            else:
                overall_status, overall_class = "Perlu Perbaikan", "quality-poor"
            
            lines.append("")
            lines.append(f"**📊 Overall Score:** <span class='{overall_class}'>{overall_status} ({overall_score:.0f}/100)</span>")
        
        lines.append("")
        lines.append("<div class='operator-section'>")
        lines.append("</div>")
    
    # RANKING
    if operator_scores:
        lines.append("")
        lines.append("---")
        lines.append("### 🏆 **Ranking Overall Performance**")
        lines.append("")
        
        sorted_ops = sorted(operator_scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (op, score) in enumerate(sorted_ops, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
            badge = "<span class='best-badge'>TERBAIK</span>" if rank == 1 else ""
            lines.append(f"{medal} **{rank}. {op}** - Score: {score:.0f}/100 {badge}")
    
    return "\n".join(lines)

# ===== MAIN APP =====
def main():
    st.markdown('<p class="main-header">📡 Dashboard QoS Telekomunikasi</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">🗺️ Peta Interaktif | 📊 Complete Analysis | <span class="tech-badge-2g">2G</span> + <span class="tech-badge-4g">4G</span></p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📁 Sumber Data")
    data_files = get_data_files(DATA_FOLDER)
    file_path = None
    
    if data_files:
        st.sidebar.success(f"✅ {len(data_files)} file")
        file_names = [os.path.basename(f) for f in data_files]
        selected_file = st.sidebar.selectbox("📂 File", file_names)
        idx = file_names.index(selected_file)
        file_path = data_files[idx]
        info = get_file_info(file_path)
        if info:
            st.sidebar.info(f"📊 {info['size']}")
    else:
        st.sidebar.warning(f"⚠️ Folder '{DATA_FOLDER}' kosong")
        uploaded = st.sidebar.file_uploader("📤 Upload", type=['xlsx', 'xls', 'csv'])
        if uploaded:
            file_path = uploaded
            st.sidebar.success(f"✅ {uploaded.name}")
        else:
            st.info(f"Buat folder `{DATA_FOLDER}` dan letakkan file di sana")
            return
    
    with st.spinner('⏳ Loading...'):
        df, error = load_and_prepare_data(file_path)
    
    if error:
        st.error(f"❌ {error}")
        return
    
    if df is None or len(df) == 0:
        st.error("❌ Tidak ada data")
        return
    
    st.sidebar.success(f"✅ {len(df):,} baris")
    
    # Filters
    st.sidebar.markdown("---")
    st.sidebar.title("🔍 Filter")
    
    kab_opts = ['Semua'] + sorted([str(k) for k in df['Kabupaten / Kota'].unique() if pd.notna(k)])
    sel_kab = st.sidebar.selectbox("📍 Kabupaten", kab_opts)
    
    df_filtered = df.copy()
    if sel_kab != 'Semua':
        df_filtered = df_filtered[df_filtered['Kabupaten / Kota'] == sel_kab]
    
    has_date = 'Tanggal_Only' in df_filtered.columns and df_filtered['Tanggal_Only'].notna().any()
    
    if has_date:
        st.sidebar.markdown("**📅 Tanggal**")
        date_type = st.sidebar.radio("", ["Semua", "Spesifik"], horizontal=True)
        if date_type == "Spesifik":
            dates = sorted(df_filtered['Tanggal_Only'].dropna().unique())
            sel_date = st.sidebar.selectbox("", dates,
                format_func=lambda x: pd.to_datetime(x).strftime('%d %B %Y'))
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
    
    # TABS - 9 tabs (Signal will include both 2G and 4G)
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "📊 Overview",
        "🗺️ Peta",
        "📡 Signal (2G + 4G)",
        "🌐 Browsing",
        "🚀 Speed Test",
        "🏓 Ping Test",
        "📹 YouTube",
        "📍 Per Lokasi",
        "📋 Kesimpulan"
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
        st.markdown("### 📈 Summary per Operator")
        
        metrics = {
            'RxLev 2G (dBm)': 'Average RxLev (2G)',
            'RxQual 2G': 'Average RxQual (2G)',
            'RSRP 4G (dBm)': 'Average RSRP (Signal Strenght 4G)',
            'DL Speed (Mbps)': 'Average Speed Test DL (Mbps) (4G)',
            'YouTube SR (%)': 'Youtube SR (%)'
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
    
    # TAB 2: PETA INTERAKTIF
    with tab2:
        st.markdown("### 🗺️ Peta Lokasi Pengukuran QoS")
        st.info("💡 Hover marker untuk melihat detail pengukuran 2G + 4G di setiap lokasi")
        
        has_coords = 'Lat' in df_filtered.columns and 'Long' in df_filtered.columns
        valid_coords = df_filtered['Lat'].notna().sum() if has_coords else 0
        
        if not has_coords:
            st.warning("⚠️ Data koordinat (Lat/Long) tidak tersedia")
        elif valid_coords == 0:
            st.warning("⚠️ Tidak ada koordinat yang valid")
        else:
            st.success(f"✅ {valid_coords} lokasi dengan koordinat valid")
            
            fig_map = create_interactive_map(df_filtered)
            
            if fig_map:
                st.plotly_chart(fig_map, use_container_width=True)
                
                st.markdown("---")
                st.markdown("### 📊 Statistik Peta")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📍 Lokasi di Peta", valid_coords)
                with col2:
                    lat_range = df_filtered['Lat'].max() - df_filtered['Lat'].min()
                    st.metric("🌍 Lat Range", f"{lat_range:.4f}°")
                with col3:
                    lon_range = df_filtered['Long'].max() - df_filtered['Long'].min()
                    st.metric("🌍 Long Range", f"{lon_range:.4f}°")
            else:
                st.error("❌ Gagal membuat peta")
    
    # TAB 3: SIGNAL (2G + 4G)
    with tab3:
        st.markdown("### 📡 Signal Quality")
        
        # 2G Section
        has_2g_data = ('Average RxLev (2G)' in df_filtered.columns or 
                      'Average RxQual (2G)' in df_filtered.columns)
        
        if has_2g_data:
            st.markdown("## 📶 2G Signal Quality")
            st.markdown('<span class="tech-badge-2g">2G Technology</span>', unsafe_allow_html=True)
            
            if 'Average RxLev (2G)' in df_filtered.columns:
                st.markdown("#### RxLev 2G (Signal Strength)")
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average RxLev (2G)': lambda x: safe_agg(x)
                })
                fig = create_signal_quality_chart(agg, 'Lokasi Pengukuran',
                    'Average RxLev (2G)', 'RxLev 2G per Lokasi (dBm)')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    st.caption("📌 Excellent: ≥-75 dBm | Good: -75 to -85 dBm | Fair: -85 to -95 dBm | Poor: <-95 dBm")
            
            if 'Average RxQual (2G)' in df_filtered.columns:
                st.markdown("#### RxQual 2G (Signal Quality)")
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average RxQual (2G)': lambda x: safe_agg(x)
                })
                fig = create_speed_chart(agg, 'Lokasi Pengukuran',
                    'Average RxQual (2G)', 'RxQual 2G per Lokasi (0=Best, 7=Worst)')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    st.caption("📌 Excellent: ≤2 | Good: 3-4 | Fair: 5 | Poor: ≥6")
            
            st.markdown("---")
        
        # 4G Section
        st.markdown("## 📡 4G Signal Quality")
        st.markdown('<span class="tech-badge-4g">4G Technology</span>', unsafe_allow_html=True)
        
        if 'Average RSRP (Signal Strenght 4G)' in df_filtered.columns:
            st.markdown("#### RSRP 4G (Signal Strength)")
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Average RSRP (Signal Strenght 4G)': lambda x: safe_agg(x)
            })
            fig = create_signal_quality_chart(agg, 'Lokasi Pengukuran',
                'Average RSRP (Signal Strenght 4G)', 'RSRP 4G per Lokasi (dBm)')
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                st.caption("📌 Excellent: ≥-80 dBm | Good: -80 to -90 dBm | Fair: -90 to -100 dBm | Poor: <-100 dBm")
        
        if 'Average RSRQ (Signal Qualty 4G)' in df_filtered.columns:
            st.markdown("#### RSRQ 4G (Signal Quality)")
            agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                'Average RSRQ (Signal Qualty 4G)': lambda x: safe_agg(x)
            })
            fig = create_signal_quality_chart(agg, 'Lokasi Pengukuran',
                'Average RSRQ (Signal Qualty 4G)', 'RSRQ 4G per Lokasi (dB)')
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    # TAB 4: BROWSING
    with tab4:
        st.markdown("### 🌐 Browsing")
        col1, col2 = st.columns(2)
        with col1:
            if 'Browsing Success (%)' in df_filtered.columns:
                st.markdown("#### Success Rate")
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Browsing Success (%)': lambda x: safe_agg(x)
                })
                fig = create_speed_chart(agg, 'Lokasi Pengukuran',
                    'Browsing Success (%)', 'Browsing Success Rate (%)')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        with col2:
            if 'Average Browsing Speed (Mbps)' in df_filtered.columns:
                st.markdown("#### Speed")
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average Browsing Speed (Mbps)': lambda x: safe_agg(x)
                })
                fig = create_speed_chart(agg, 'Lokasi Pengukuran',
                    'Average Browsing Speed (Mbps)', 'Browsing Speed (Mbps)')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    # TAB 5: SPEED TEST
    with tab5:
        st.markdown("### 🚀 Speed Test")
        col1, col2 = st.columns(2)
        with col1:
            if 'Average Speed Test DL (Mbps) (4G)' in df_filtered.columns:
                st.markdown("#### Download")
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average Speed Test DL (Mbps) (4G)': lambda x: safe_agg(x)
                })
                fig = create_speed_chart(agg, 'Lokasi Pengukuran',
                    'Average Speed Test DL (Mbps) (4G)', 'Download Speed 4G')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        with col2:
            if 'Average Speed Test UL (Mbps) (4G)' in df_filtered.columns:
                st.markdown("#### Upload")
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average Speed Test UL (Mbps) (4G)': lambda x: safe_agg(x)
                })
                fig = create_speed_chart(agg, 'Lokasi Pengukuran',
                    'Average Speed Test UL (Mbps) (4G)', 'Upload Speed 4G')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    # TAB 6: PING TEST
    with tab6:
        st.markdown("### 🏓 Ping Test")
        col1, col2 = st.columns(2)
        with col1:
            if 'Average RTT Latency (ms)' in df_filtered.columns:
                st.markdown("#### Latency")
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average RTT Latency (ms)': lambda x: safe_agg(x)
                })
                fig = create_speed_chart(agg, 'Lokasi Pengukuran',
                    'Average RTT Latency (ms)', 'Ping Latency (Lower is Better)')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        with col2:
            if 'Packet Loss (%)' in df_filtered.columns:
                st.markdown("#### Packet Loss")
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Packet Loss (%)': lambda x: safe_agg(x)
                })
                fig = create_speed_chart(agg, 'Lokasi Pengukuran',
                    'Packet Loss (%)', 'Packet Loss (Lower is Better)')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    # TAB 7: YOUTUBE
    with tab7:
        st.markdown("### 📹 YouTube")
        col1, col2 = st.columns(2)
        with col1:
            if 'Youtube SR (%)' in df_filtered.columns:
                st.markdown("#### Success Rate")
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Youtube SR (%)': lambda x: safe_agg(x)
                })
                fig = create_speed_chart(agg, 'Lokasi Pengukuran',
                    'Youtube SR (%)', 'YouTube Success Rate (%)')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        with col2:
            if 'Average TTFP (s)' in df_filtered.columns:
                st.markdown("#### TTFP")
                agg = df_filtered.groupby(['Lokasi Pengukuran', 'Operator'], as_index=False).agg({
                    'Average TTFP (s)': lambda x: safe_agg(x)
                })
                fig = create_speed_chart(agg, 'Lokasi Pengukuran',
                    'Average TTFP (s)', 'YouTube TTFP (Lower is Better)')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    # TAB 8: PER LOKASI
    with tab8:
        st.markdown("### 📍 Per Lokasi")
        locations = sorted(df_filtered['Lokasi Pengukuran'].unique())
        if locations:
            sel_loc = st.selectbox("Pilih Lokasi", locations)
            df_loc = df_filtered[df_filtered['Lokasi Pengukuran'] == sel_loc]
            
            st.markdown(f"#### {sel_loc}")
            
            detail_cols = [
                'Average RxLev (2G)',
                'Average RxQual (2G)',
                'Average RSRP (Signal Strenght 4G)',
                'Average Speed Test DL (Mbps) (4G)',
                'Youtube SR (%)',
                'Average RTT Latency (ms)'
            ]
            
            avail = [c for c in detail_cols if c in df_loc.columns]
            if avail:
                detail = df_loc.groupby('Operator')[avail].agg(lambda x: safe_agg(x)).round(2)
                st.dataframe(detail, use_container_width=True)
    
    # TAB 9: KESIMPULAN
    with tab9:
        st.markdown("### 📋 Kesimpulan Detail")
        st.info("💡 Kesimpulan per tanggal untuk SEMUA operator (2G + 4G)")
        
        if not has_date:
            st.warning("⚠️ Data tanggal tidak tersedia")
            return
        
        groupby_cols = ['Lokasi Pengukuran', 'Tanggal_Only']
        grouped = df_filtered.groupby(groupby_cols)
        total = len(grouped)
        
        st.markdown(f"**📊 Total: {total} kombinasi**")
        
        per_page = 3
        total_pages = (total + per_page - 1) // per_page
        page = st.selectbox("Halaman", range(1, total_pages + 1))
        
        start = (page - 1) * per_page
        end = min(start + per_page, total)
        
        for idx, (keys, data) in enumerate(list(grouped)[start:end], start=start + 1):
            loc, date = keys
            date_str = pd.to_datetime(date).strftime('%d %B %Y')
            title = f"📌 {idx}. {loc} - {date_str}"
            
            with st.expander(title, expanded=(idx == start + 1)):
                conclusion = generate_detailed_conclusion_per_date(data, loc, date_str)
                st.markdown(f"<div class='conclusion-card'>{conclusion}</div>", unsafe_allow_html=True)
        
        st.caption(f"Menampilkan {start + 1}-{end} dari {total}")

if __name__ == "__main__":
    main()