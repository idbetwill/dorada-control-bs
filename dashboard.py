import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from database import DatabaseManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Dorada Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Alcaldía de La Dorada color palette
st.markdown("""
<style>
    /* Alcaldía de La Dorada Color Palette - Red Dominant */
    :root {
        --dorada-red: #D32F2F;
        --dorada-light-red: #F44336;
        --dorada-dark-red: #B71C1C;
        --dorada-green: #2E7D32;
        --dorada-yellow: #FFC107;
        --dorada-orange: #FF9800;
        --dorada-blue: #1976D2;
        --dorada-purple: #7B1FA2;
        --dorada-grey: #757575;
        --dorada-light-green: #4CAF50;
        --dorada-light-yellow: #FFEB3B;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: var(--dorada-red);
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, var(--dorada-red) 0%, var(--dorada-dark-red) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .dorada-header {
        background: linear-gradient(135deg, var(--dorada-red) 0%, var(--dorada-dark-red) 100%);
        color: white;
        padding: 1rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(211, 47, 47, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--dorada-red) 0%, var(--dorada-dark-red) 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 2px solid var(--dorada-yellow);
        box-shadow: 0 8px 32px rgba(211, 47, 47, 0.2);
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(211, 47, 47, 0.4);
    }
    
    .stMetric {
        background: linear-gradient(135deg, var(--dorada-red) 0%, var(--dorada-dark-red) 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 8px 32px rgba(211, 47, 47, 0.2);
        color: white;
        border: 2px solid var(--dorada-yellow);
        transition: transform 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(211, 47, 47, 0.4);
    }
    
    .stMetric > div {
        color: white !important;
    }
    .stMetric > div > div {
        color: white !important;
    }
    .stMetric > div > div > div {
        color: white !important;
    }
    
    .stSubheader {
        color: var(--dorada-red);
        font-weight: bold;
        font-size: 1.5rem;
        margin: 1rem 0;
        padding: 0.5rem;
        border-left: 4px solid var(--dorada-red);
        background: linear-gradient(90deg, #f8f9fa 0%, #ffebee 100%);
        border-radius: 0.5rem;
    }
    
    .stDataFrame {
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 16px rgba(211, 47, 47, 0.1);
        border: 1px solid var(--dorada-red);
    }
    
    .stSelectbox {
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 16px rgba(211, 47, 47, 0.1);
        border: 1px solid var(--dorada-red);
    }
    
    .stSlider {
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 16px rgba(211, 47, 47, 0.1);
        border: 1px solid var(--dorada-red);
    }
    
    .stTextInput {
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 16px rgba(211, 47, 47, 0.1);
        border: 1px solid var(--dorada-red);
    }
    
    /* Fix dropdown positioning for autocomplete */
    .stTextInput > div > div > div > div {
        position: relative !important;
    }
    .stTextInput .stAutocomplete > div > div {
        position: absolute !important;
        top: 100% !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 1000 !important;
        background: white !important;
        border: 1px solid var(--dorada-red) !important;
        border-radius: 0.5rem !important;
        box-shadow: 0 4px 16px rgba(211, 47, 47, 0.2) !important;
        max-height: 200px !important;
        overflow-y: auto !important;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--dorada-red) 0%, var(--dorada-dark-red) 100%);
        color: white;
    }
    
    .sidebar .sidebar-content .stSelectbox {
        background: rgba(255,255,255,0.95);
        color: var(--dorada-red);
        border: 1px solid var(--dorada-yellow);
    }
    
    .stPlotlyChart {
        background: white;
        border-radius: 1rem;
        box-shadow: 0 8px 32px rgba(211, 47, 47, 0.1);
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid var(--dorada-red);
    }
    
    .stWarning {
        background: linear-gradient(135deg, var(--dorada-yellow) 0%, var(--dorada-orange) 100%);
        border: 2px solid var(--dorada-orange);
        border-radius: 1rem;
        padding: 1rem;
        color: #8b4513;
    }
    
    .stError {
        background: linear-gradient(135deg, var(--dorada-red) 0%, var(--dorada-light-red) 100%);
        border: 2px solid var(--dorada-red);
        border-radius: 1rem;
        padding: 1rem;
        color: white;
    }
    
    .dorada-success {
        background: linear-gradient(135deg, var(--dorada-green) 0%, var(--dorada-light-green) 100%);
        border: 2px solid var(--dorada-green);
        border-radius: 1rem;
        padding: 1rem;
        color: white;
    }
    
    .dorada-info {
        background: linear-gradient(135deg, var(--dorada-blue) 0%, var(--dorada-purple) 100%);
        border: 2px solid var(--dorada-blue);
        border-radius: 1rem;
        padding: 1rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_data():
    """Load data from database with caching"""
    try:
        db_manager = DatabaseManager()
        if db_manager.connect():
            cumplimiento_df = db_manager.get_cumplimiento_data()
            financiero_df = db_manager.get_financiero_data()
            db_manager.close()
            return cumplimiento_df, financiero_df
        else:
            st.error("No se pudo conectar a la base de datos")
            return pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return pd.DataFrame(), pd.DataFrame()

def main():
    """Main dashboard function"""
    
    # Header with Alcaldía de La Dorada branding
    st.markdown("""
    <div class="dorada-header">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: bold;">
            🏛️ ALCALDÍA DE LA DORADA
        </h1>
        <h2 style="margin: 0.5rem 0 0 0; font-size: 1.8rem; font-weight: 300;">
            Sistema de Seguimiento y Control del Plan de Desarrollo
        </h2>
        <h3 style="margin: 0.5rem 0 0 0; font-size: 1.2rem; font-weight: 300;">
            "La Fuerza de las Ideas" 2024-2027
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    cumplimiento_df, financiero_df = load_data()
    
    # Sidebar with Dorada red branding
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%); border-radius: 1rem; margin-bottom: 2rem;">
        <h3 style="color: white; margin: 0; font-size: 1.2rem;">🏛️ ALCALDÍA DE LA DORADA</h3>
        <p style="color: white; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Sistema de Control</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("### 🎛️ Controles")
    
    # Data source selection
    data_source = st.sidebar.selectbox(
        "Seleccionar fuente de datos:",
        ["Cumplimiento Plan Desarrollo", "Reporte Financiero"]
    )
    
    # Additional sidebar information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Información del Sistema")
    
    if data_source == "Cumplimiento Plan Desarrollo":
        st.sidebar.markdown("""
        <div style="background: linear-gradient(135deg, #F44336 0%, #D32F2F 100%); padding: 1rem; border-radius: 0.5rem; color: white;">
            <h4 style="margin: 0 0 0.5rem 0;">📈 Cumplimiento</h4>
            <p style="margin: 0; font-size: 0.9rem;">Seguimiento de indicadores del Plan de Desarrollo "La Fuerza de las Ideas"</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div style="background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%); padding: 1rem; border-radius: 0.5rem; color: white;">
            <h4 style="margin: 0 0 0.5rem 0;">💰 Financiero</h4>
            <p style="margin: 0; font-size: 0.9rem;">Análisis de presupuesto y ejecución financiera</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📅 Última Actualización")
    st.sidebar.markdown(f"**Fecha:** {pd.Timestamp.now().strftime('%d/%m/%Y')}")
    st.sidebar.markdown(f"**Hora:** {pd.Timestamp.now().strftime('%H:%M')}")
    
    # Main content
    if data_source == "Cumplimiento Plan Desarrollo":
        display_cumplimiento_dashboard(cumplimiento_df)
    else:
        display_financiero_dashboard(financiero_df)

def display_cumplimiento_dashboard(df):
    """Display development plan compliance dashboard"""
    
    if df.empty:
        st.warning("No hay datos de cumplimiento disponibles")
        return
    
    # Filters section
    st.markdown('<h3 class="stSubheader">🔍 Filtros de Búsqueda</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        # Filter by Eje
        ejes = ['Todos'] + sorted(df['eje'].unique().tolist())
        eje_filter = st.selectbox("Eje:", ejes)
    
    with col2:
        # Filter by Secretaría
        secretarias = ['Todas'] + sorted(df['secretaria'].unique().tolist())
        secretaria_filter = st.selectbox("Secretaría:", secretarias)
    
    with col3:
        # Filter by Dependencia
        dependencias = ['Todas'] + sorted(df['dependencia'].unique().tolist())
        dependencia_filter = st.selectbox("Dependencia:", dependencias)
    
    with col4:
        # Filter by Sector
        sectores = ['Todos'] + sorted(df['sector'].unique().tolist())
        sector_filter = st.selectbox("Sector:", sectores)
    
    with col5:
        # Filter by Programa
        programas = ['Todos'] + sorted(df['programa'].unique().tolist())
        programa_filter = st.selectbox("Programa:", programas)
    
    # Apply filters
    filtered_df = df.copy()
    
    if eje_filter != 'Todos':
        filtered_df = filtered_df[filtered_df['eje'] == eje_filter]
    
    if secretaria_filter != 'Todas':
        filtered_df = filtered_df[filtered_df['secretaria'] == secretaria_filter]
    
    if dependencia_filter != 'Todas':
        filtered_df = filtered_df[filtered_df['dependencia'] == dependencia_filter]
    
    if sector_filter != 'Todos':
        filtered_df = filtered_df[filtered_df['sector'] == sector_filter]
    
    if programa_filter != 'Todos':
        filtered_df = filtered_df[filtered_df['programa'] == programa_filter]
    
    # Show filter results
    st.info(f"📊 Mostrando {len(filtered_df)} de {len(df)} indicadores")
    
    # Key metrics with better styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_cumplimiento = filtered_df['porcentaje_cumplimiento'].mean()
        st.metric("Promedio Cumplimiento", f"{avg_cumplimiento:.1f}%", delta=f"{avg_cumplimiento:.1f}%")
    
    with col2:
        total_indicadores = len(filtered_df)
        st.metric("Total Indicadores", total_indicadores, delta=total_indicadores)
    
    with col3:
        cumplimiento_alto = len(filtered_df[filtered_df['porcentaje_cumplimiento'] >= 80])
        st.metric("Cumplimiento Alto (≥80%)", cumplimiento_alto, delta=cumplimiento_alto)
    
    with col4:
        cumplimiento_bajo = len(filtered_df[filtered_df['porcentaje_cumplimiento'] < 50])
        st.metric("Cumplimiento Bajo (<50%)", cumplimiento_bajo, delta=cumplimiento_bajo)
    
    # Charts with better styling
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="stSubheader">📈 Distribución de Cumplimiento</h3>', unsafe_allow_html=True)
        
        # Create histogram with Dorada red color palette
        fig_hist = px.histogram(
            filtered_df, 
            x='porcentaje_cumplimiento',
            nbins=20,
            title="Distribución de Porcentajes de Cumplimiento",
            labels={'porcentaje_cumplimiento': 'Porcentaje de Cumplimiento (%)', 'count': 'Cantidad de Indicadores'},
            color_discrete_sequence=['#D32F2F'],  # Dorada red
            opacity=0.8
        )
        fig_hist.update_layout(
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),  # Black text
            title_font_size=16,
            title_font_color='#D32F2F',  # Dorada red
            title_x=0.5
        )
        fig_hist.update_xaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        fig_hist.update_yaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="stSubheader">🎯 Top 10 Indicadores</h3>', unsafe_allow_html=True)
        
        # Top 10 indicators by compliance
        top_indicators = filtered_df.nlargest(10, 'porcentaje_cumplimiento')
        
        fig_bar = px.bar(
            top_indicators,
            x='porcentaje_cumplimiento',
            y='indicador',
            orientation='h',
            title="Top 10 Indicadores por Cumplimiento",
            labels={'porcentaje_cumplimiento': 'Porcentaje (%)', 'indicador': 'Indicador'},
            color='porcentaje_cumplimiento',
            color_continuous_scale=['#FFC107', '#FF9800', '#D32F2F']  # Dorada yellow, orange, red
        )
        fig_bar.update_layout(
            yaxis={'categoryorder':'total ascending'},
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),  # Black text
            title_font_size=16,
            title_font_color='#D32F2F',  # Dorada red
            title_x=0.5
        )
        fig_bar.update_xaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        fig_bar.update_yaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # New section: Avance por Eje
    st.markdown('<h3 class="stSubheader">🎯 Avance por Eje del Plan de Desarrollo</h3>', unsafe_allow_html=True)
    
    # Calculate progress by axis
    eje_progress = filtered_df.groupby('eje').agg({
        'porcentaje_cumplimiento': 'mean',
        'indicador': 'count',
        'meta_anual': 'sum',
        'avance_actual': 'sum'
    }).round(2).reset_index()
    
    eje_progress.columns = ['Eje', 'Promedio Cumplimiento (%)', 'Cantidad Indicadores', 'Meta Total', 'Avance Total']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart showing progress by axis
        fig_eje = px.bar(
            eje_progress,
            x='Eje',
            y='Promedio Cumplimiento (%)',
            title="Promedio de Cumplimiento por Eje",
            labels={'Promedio Cumplimiento (%)': 'Promedio (%)', 'Eje': 'Eje del Plan'},
            color='Promedio Cumplimiento (%)',
            color_continuous_scale=['#FFC107', '#FF9800', '#D32F2F']  # Dorada yellow, orange, red
        )
        fig_eje.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),  # Black text
            title_font_size=16,
            title_font_color='#D32F2F',  # Dorada red
            title_x=0.5,
            xaxis_tickangle=-45
        )
        fig_eje.update_xaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        fig_eje.update_yaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        st.plotly_chart(fig_eje, use_container_width=True)
    
    with col2:
        # Table showing detailed progress by axis
        st.markdown('<h4 style="color: #D32F2F;">📊 Detalle por Eje</h4>', unsafe_allow_html=True)
        st.dataframe(
            eje_progress,
            use_container_width=True,
            height=300
        )
    
    # Additional chart
    st.markdown('<h3 class="stSubheader">📊 Comparación Meta vs Avance</h3>', unsafe_allow_html=True)
    
    # Create comparison chart
    fig_comp = go.Figure()
    
    fig_comp.add_trace(go.Bar(
        name='Meta Anual',
        x=filtered_df['indicador'],
        y=filtered_df['meta_anual'],
        marker_color='#D32F2F',  # Dorada red
        opacity=0.8
    ))
    
    fig_comp.add_trace(go.Bar(
        name='Avance Actual',
        x=filtered_df['indicador'],
        y=filtered_df['avance_actual'],
        marker_color='#FFC107',  # Dorada yellow
        opacity=0.8
    ))
    
    fig_comp.update_layout(
        title="Comparación Meta Anual vs Avance Actual",
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#000000'),  # Black text
        title_font_size=16,
        title_font_color='#D32F2F',  # Dorada red
        title_x=0.5,
        xaxis_tickangle=-45
    )
    fig_comp.update_xaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
    fig_comp.update_yaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
    
    st.plotly_chart(fig_comp, use_container_width=True)
    
    # Detailed table
    st.markdown('<h3 class="stSubheader">📋 Detalle de Indicadores</h3>', unsafe_allow_html=True)
    
    # Add filters
    col1, col2 = st.columns(2)
    
    with col1:
        min_cumplimiento = st.slider(
            "Cumplimiento mínimo (%)",
            min_value=0,
            max_value=100,
            value=0
        )
    
    with col2:
        search_term = st.text_input("Buscar indicador:", "")
    
    # Apply additional filters to already filtered data
    detailed_filtered = filtered_df.copy()
    if min_cumplimiento > 0:
        detailed_filtered = detailed_filtered[detailed_filtered['porcentaje_cumplimiento'] >= min_cumplimiento]
    
    if search_term:
        detailed_filtered = detailed_filtered[detailed_filtered['indicador'].str.contains(search_term, case=False, na=False)]
    
    # Display table with better styling
    st.dataframe(
        detailed_filtered[['indicador', 'eje', 'secretaria', 'dependencia', 'sector', 'programa', 'meta_anual', 'avance_actual', 'porcentaje_cumplimiento']].rename(
            columns={
                'indicador': 'Indicador',
                'eje': 'Eje',
                'secretaria': 'Secretaría',
                'dependencia': 'Dependencia',
                'sector': 'Sector',
                'programa': 'Programa',
                'meta_anual': 'Meta Anual',
                'avance_actual': 'Avance Actual',
                'porcentaje_cumplimiento': '% Cumplimiento'
            }
        ),
        use_container_width=True,
        height=400
    )

def display_financiero_dashboard(df):
    """Display financial report dashboard"""
    
    if df.empty:
        st.warning("No hay datos financieros disponibles")
        return
    
    # Filters section
    st.markdown('<h3 class="stSubheader">🔍 Filtros de Búsqueda</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Filter by Eje
        ejes = ['Todos'] + sorted(df['eje'].unique().tolist())
        eje_filter = st.selectbox("Eje:", ejes)
    
    with col2:
        # Filter by Dependencia
        dependencias = ['Todas'] + sorted(df['dependencia'].unique().tolist())
        dependencia_filter = st.selectbox("Dependencia:", dependencias)
    
    with col3:
        # Filter by Sector
        sectores = ['Todos'] + sorted(df['sector'].unique().tolist())
        sector_filter = st.selectbox("Sector:", sectores)
    
    with col4:
        # Filter by Programa
        programas = ['Todos'] + sorted(df['programa'].unique().tolist())
        programa_filter = st.selectbox("Programa:", programas)
    
    # Apply filters
    filtered_df = df.copy()
    
    if eje_filter != 'Todos':
        filtered_df = filtered_df[filtered_df['eje'] == eje_filter]
    
    if dependencia_filter != 'Todas':
        filtered_df = filtered_df[filtered_df['dependencia'] == dependencia_filter]
    
    if sector_filter != 'Todos':
        filtered_df = filtered_df[filtered_df['sector'] == sector_filter]
    
    if programa_filter != 'Todos':
        filtered_df = filtered_df[filtered_df['programa'] == programa_filter]
    
    # Show filter results
    st.info(f"📊 Mostrando {len(filtered_df)} de {len(df)} conceptos financieros")
    
    # Key metrics with better styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_presupuesto = filtered_df['presupuesto_anual'].sum()
        st.metric("Presupuesto Total", f"${total_presupuesto:,.0f}", delta=f"${total_presupuesto:,.0f}")
    
    with col2:
        total_ejecutado = filtered_df['ejecutado'].sum()
        st.metric("Total Ejecutado", f"${total_ejecutado:,.0f}", delta=f"${total_ejecutado:,.0f}")
    
    with col3:
        total_disponible = filtered_df['disponible'].sum()
        st.metric("Total Disponible", f"${total_disponible:,.0f}", delta=f"${total_disponible:,.0f}")
    
    with col4:
        avg_ejecucion = filtered_df['porcentaje_ejecucion'].mean()
        st.metric("Promedio Ejecución", f"{avg_ejecucion:.1f}%", delta=f"{avg_ejecucion:.1f}%")
    
    # Charts with better styling
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="stSubheader">💰 Distribución Presupuestaria</h3>', unsafe_allow_html=True)
        
        # Create pie chart for budget distribution with Dorada red colors
        fig_pie = px.pie(
            filtered_df.head(10),  # Limit to top 10 for better visualization
            values='presupuesto_anual',
            names='concepto',
            title="Distribución del Presupuesto Anual (Top 10)",
            color_discrete_sequence=['#D32F2F', '#F44336', '#E57373', '#FFCDD2', '#FFC107', '#FF9800', '#FF5722', '#B71C1C', '#9C27B0', '#3F51B5']
        )
        fig_pie.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),  # Black text
            title_font_size=16,
            title_font_color='#D32F2F',  # Dorada red
            title_x=0.5
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="stSubheader">📊 Ejecución vs Presupuesto</h3>', unsafe_allow_html=True)
        
        # Create bar chart comparing budget vs executed with Dorada red colors
        fig_bar = px.bar(
            filtered_df.head(10),
            x='concepto',
            y=['presupuesto_anual', 'ejecutado'],
            title="Presupuesto vs Ejecutado (Top 10)",
            barmode='group',
            color_discrete_map={'presupuesto_anual': '#D32F2F', 'ejecutado': '#FFC107'}  # Dorada red and yellow
        )
        fig_bar.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),  # Black text
            title_font_size=16,
            title_font_color='#D32F2F',  # Dorada red
            title_x=0.5
        )
        fig_bar.update_xaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        fig_bar.update_yaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # New section: Avance por Eje
    st.markdown('<h3 class="stSubheader">🎯 Avance Financiero por Eje</h3>', unsafe_allow_html=True)
    
    # Calculate financial progress by axis
    eje_financiero = filtered_df.groupby('eje').agg({
        'porcentaje_ejecucion': 'mean',
        'concepto': 'count',
        'presupuesto_anual': 'sum',
        'ejecutado': 'sum'
    }).round(2).reset_index()
    
    eje_financiero.columns = ['Eje', 'Promedio Ejecución (%)', 'Cantidad Conceptos', 'Presupuesto Total', 'Ejecutado Total']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart showing financial progress by axis
        fig_eje_fin = px.bar(
            eje_financiero,
            x='Eje',
            y='Promedio Ejecución (%)',
            title="Promedio de Ejecución Financiera por Eje",
            labels={'Promedio Ejecución (%)': 'Promedio (%)', 'Eje': 'Eje del Plan'},
            color='Promedio Ejecución (%)',
            color_continuous_scale=['#FFC107', '#FF9800', '#D32F2F']  # Dorada yellow, orange, red
        )
        fig_eje_fin.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),  # Black text
            title_font_size=16,
            title_font_color='#D32F2F',  # Dorada red
            title_x=0.5,
            xaxis_tickangle=-45
        )
        fig_eje_fin.update_xaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        fig_eje_fin.update_yaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        st.plotly_chart(fig_eje_fin, use_container_width=True)
    
    with col2:
        # Table showing detailed financial progress by axis
        st.markdown('<h4 style="color: #D32F2F;">📊 Detalle Financiero por Eje</h4>', unsafe_allow_html=True)
        st.dataframe(
            eje_financiero,
            use_container_width=True,
            height=300
        )
    
    # Additional charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="stSubheader">📈 Porcentaje de Ejecución</h3>', unsafe_allow_html=True)
        
        # Scatter plot of budget vs execution percentage with Dorada red colors
        fig_scatter = px.scatter(
            filtered_df.head(20),
            x='presupuesto_anual',
            y='porcentaje_ejecucion',
            size='ejecutado',
            hover_data=['concepto'],
            title="Presupuesto vs % Ejecución",
            color='porcentaje_ejecucion',
            color_continuous_scale=['#FFC107', '#FF9800', '#D32F2F']  # Dorada yellow, orange, red
        )
        fig_scatter.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),  # Black text
            title_font_size=16,
            title_font_color='#D32F2F',  # Dorada red
            title_x=0.5
        )
        fig_scatter.update_xaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        fig_scatter.update_yaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="stSubheader">🎯 Top Ejecutores</h3>', unsafe_allow_html=True)
        
        # Top 10 by execution amount
        top_ejecutores = filtered_df.nlargest(10, 'ejecutado')
        
        fig_bar2 = px.bar(
            top_ejecutores,
            x='ejecutado',
            y='concepto',
            orientation='h',
            title="Top 10 por Monto Ejecutado",
            color='ejecutado',
            color_continuous_scale=['#FFC107', '#FF9800', '#D32F2F']  # Dorada yellow, orange, red
        )
        fig_bar2.update_layout(
            yaxis={'categoryorder':'total ascending'},
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#000000'),  # Black text
            title_font_size=16,
            title_font_color='#D32F2F',  # Dorada red
            title_x=0.5
        )
        fig_bar2.update_xaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        fig_bar2.update_yaxes(gridcolor='#ffebee', zerolinecolor='#D32F2F', tickfont=dict(color='#000000'))
        st.plotly_chart(fig_bar2, use_container_width=True)
    
    # Detailed table
    st.markdown('<h3 class="stSubheader">📋 Detalle Financiero</h3>', unsafe_allow_html=True)
    
    # Add filters
    col1, col2 = st.columns(2)
    
    with col1:
        min_ejecucion = st.slider(
            "Ejecución mínima (%)",
            min_value=0,
            max_value=100,
            value=0
        )
    
    with col2:
        search_term = st.text_input("Buscar concepto:", "")
    
    # Apply additional filters to already filtered data
    detailed_filtered = filtered_df.copy()
    if min_ejecucion > 0:
        detailed_filtered = detailed_filtered[detailed_filtered['porcentaje_ejecucion'] >= min_ejecucion]
    
    if search_term:
        detailed_filtered = detailed_filtered[detailed_filtered['concepto'].str.contains(search_term, case=False, na=False)]
    
    # Display table with better styling
    st.dataframe(
        detailed_filtered[['concepto', 'eje', 'dependencia', 'sector', 'programa', 'presupuesto_anual', 'ejecutado', 'disponible', 'porcentaje_ejecucion']].rename(
            columns={
                'concepto': 'Concepto',
                'eje': 'Eje',
                'dependencia': 'Dependencia',
                'sector': 'Sector',
                'programa': 'Programa',
                'presupuesto_anual': 'Presupuesto Anual',
                'ejecutado': 'Ejecutado',
                'disponible': 'Disponible',
                'porcentaje_ejecucion': '% Ejecución'
            }
        ),
        use_container_width=True,
        height=400
    )

if __name__ == "__main__":
    main() 