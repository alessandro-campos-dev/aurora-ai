import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json

# Configuração da página
st.set_page_config(
    page_title="Aurora AI - Painel de Controle",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .emergencia { border-left-color: #EF4444 !important; }
    .urgente { border-left-color: #F59E0B !important; }
    .prioritario { border-left-color: #10B981 !important; }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">🏥 Aurora AI - Painel de Controle</h1>', unsafe_allow_html=True)
st.markdown("### Sistema Inteligente de Triagem e Gestão de Filas")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3026/3026959.png", width=80)
    st.title("Configurações")
    
    # Filtros
    st.subheader("📅 Filtros")
    data_inicio = st.date_input("Data Início", datetime.now() - timedelta(days=7))
    data_fim = st.date_input("Data Fim", datetime.now())
    
    unidade = st.selectbox(
        "Unidade de Saúde",
        ["Todas as Unidades", "UPA Centro", "UPA Zona Norte", "Hospital Municipal", "UBS Jardim Saúde"]
    )
    
    st.divider()
    
    # Status do sistema
    st.subheader("🟢 Status do Sistema")
    st.progress(85, text="Performance: 85%")
    st.caption("🟢 IA de Triagem: Operacional")
    st.caption("🟢 Banco de Dados: Conectado")
    st.caption("🟡 API: 98.5% uptime")
    
    st.divider()
    
    # Ações rápidas
    st.subheader("⚡ Ações Rápidas")
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.rerun()
    
    if st.button("📊 Gerar Relatório", use_container_width=True):
        st.toast("Relatório sendo gerado...", icon="📄")

# Conteúdo principal - Layout em colunas
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container():
        st.markdown('<div class="metric-card emergencia">', unsafe_allow_html=True)
        st.metric("🚨 Emergências", "24", "+3 hoje", delta_color="inverse")
        st.caption("Atendimento imediato")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="metric-card urgente">', unsafe_allow_html=True)
        st.metric("⚠️ Urgências", "42", "+8 hoje")
        st.caption("Atendimento em 1h")
        st.markdown('</div>', unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown('<div class="metric-card prioritario">', unsafe_allow_html=True)
        st.metric("📋 Prioritários", "68", "-5 hoje")
        st.caption("Atendimento em 4h")
        st.markdown('</div>', unsafe_allow_html=True)

with col4:
    with st.container():
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("⏱️ Tempo Médio", "25 min", "-40%")
        st.caption("Redução histórica")
        st.markdown('</div>', unsafe_allow_html=True)

# Divisor
st.divider()

# Gráficos principais
col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.subheader("📈 Distribuição por Prioridade (24h)")
    
    # Dados de exemplo
    dados_prioridade = pd.DataFrame({
        'Prioridade': ['Emergência', 'Urgente', 'Prioritário', 'Eletivo'],
        'Quantidade': [24, 42, 68, 35],
        'Cor': ['#EF4444', '#F59E0B', '#10B981', '#3B82F6']
    })
    
    fig1 = px.bar(
        dados_prioridade,
        x='Prioridade',
        y='Quantidade',
        color='Cor',
        color_discrete_map="identity",
        text='Quantidade'
    )
    fig1.update_traces(textposition='outside')
    fig1.update_layout(
        height=400,
        showlegend=False,
        yaxis_title="Número de Pacientes",
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_grafico2:
    st.subheader("🌡️ Sintomas Mais Comuns")
    
    sintomas = {
        'Febre': 45,
        'Dor Abdominal': 38,
        'Dor de Cabeça': 32,
        'Tosse': 28,
        'Náusea': 25,
        'Dor no Peito': 18,
        'Falta de Ar': 15,
        'Tontura': 12
    }
    
    fig2 = px.pie(
        values=list(sintomas.values()),
        names=list(sintomas.keys()),
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# Tabela de casos recentes
st.subheader("📋 Casos Recentes - Últimas 2 Horas")

# Dados de exemplo
casos_recentes = pd.DataFrame({
    'Hora': ['14:30', '14:15', '14:00', '13:45', '13:30', '13:15'],
    'Paciente': 'Paciente ' + pd.Series(range(1, 7)).astype(str),
    'Idade': [45, 32, 68, 28, 55, 39],
    'Sintomas': ['Febre + Tosse', 'Dor abdominal', 'Dor no peito', 'Náusea', 'Dor de cabeça', 'Tontura'],
    'Prioridade': ['Urgente', 'Prioritário', 'Emergência', 'Prioritário', 'Eletivo', 'Urgente'],
    'Tempo Estimado': ['45 min', '2h', 'IMEDIATO', '1.5h', '4h', '30 min']
})

# Adiciona cores condicionais
def color_priority(val):
    if val == 'Emergência':
        return 'color: #EF4444; font-weight: bold'
    elif val == 'Urgente':
        return 'color: #F59E0B; font-weight: bold'
    elif val == 'Prioritário':
        return 'color: #10B981'
    else:
        return 'color: #6B7280'

st.dataframe(
    casos_recentes.style.applymap(color_priority, subset=['Prioridade']),
    use_container_width=True,
    hide_index=True
)

# Rodapé
st.divider()
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.caption("🔄 Última atualização: " + datetime.now().strftime("%H:%M:%S"))
    
with col_info2:
    st.caption("📊 Total de triagens hoje: 342")

with col_info3:
    st.caption("🎯 Precisão da IA: 94.2%")

# Mensagem de status
with st.expander("🔍 Detalhes Técnicos do Sistema"):
    st.code("""
    Sistema: Aurora AI v1.2.0
    Status: OPERACIONAL
    IA de Triagem: BERT-multilingual (94.2% acurácia)
    Modelo de Fila: Algoritmo adaptativo
    Latência API: < 120ms
    Uptime: 99.8% (últimos 30 dias)
    """)
