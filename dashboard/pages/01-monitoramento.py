import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Monitoramento em Tempo Real",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Monitoramento em Tempo Real")
st.markdown("### Análise detalhada de fluxo e desempenho do sistema")

# Dados simulados de séries temporais
@st.cache_data(ttl=60)
def gerar_dados_monitoramento():
    horas = pd.date_range(start=datetime.now() - timedelta(hours=12), 
                         end=datetime.now(), freq='15min')
    
    dados = pd.DataFrame({
        'hora': horas,
        'pacientes_entrada': np.random.poisson(8, len(horas)).cumsum(),
        'pacientes_atendidos': np.random.poisson(7, len(horas)).cumsum(),
        'tempo_medio_espera': np.random.uniform(15, 45, len(horas)),
        'classificacoes_ia': np.random.randint(20, 50, len(horas))
    })
    return dados

dados = gerar_dados_monitoramento()

# Métricas em tempo real
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Pacientes na Fila", 
              f"{dados['pacientes_entrada'].iloc[-1] - dados['pacientes_atendidos'].iloc[-1]:.0f}",
              delta=f"+{np.random.randint(1,5)}")

with col2:
    st.metric("⚡ Taxa de Atendimento", 
              f"{dados['pacientes_atendidos'].iloc[-1]/dados['pacientes_entrada'].iloc[-1]*100:.1f}%",
              delta="+2.3%")

with col3:
    st.metric("⏱️ Tempo Médio de Espera", 
              f"{dados['tempo_medio_espera'].iloc[-1]:.0f} min",
              delta=f"-{np.random.randint(1,10)} min")

with col4:
    st.metric("🤖 Triagens IA/Hora", 
              f"{dados['classificacoes_ia'].iloc[-1]:.0f}",
              delta=f"+{np.random.randint(1,8)}")

st.divider()

# Gráfico 1: Fluxo de pacientes
st.subheader("📈 Fluxo de Pacientes - Últimas 12 Horas")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=dados['hora'],
    y=dados['pacientes_entrada'],
    name='Entradas',
    line=dict(color='#3B82F6', width=3),
    fill='tozeroy',
    fillcolor='rgba(59, 130, 246, 0.1)'
))
fig1.add_trace(go.Scatter(
    x=dados['hora'],
    y=dados['pacientes_atendidos'],
    name='Atendidos',
    line=dict(color='#10B981', width=3),
    fill='tonexty',
    fillcolor='rgba(16, 185, 129, 0.1)'
))

fig1.update_layout(
    height=400,
    xaxis_title="Horário",
    yaxis_title="Número de Pacientes",
    hovermode='x unified',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Heatmap de demanda por hora
st.subheader("🔥 Heatmap de Demanda - Padrão Diário")

# Dados simulados para heatmap
dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
horas_dia = [f'{h:02d}:00' for h in range(6, 24)]

# Matriz de demanda
demanda = np.random.randint(10, 100, size=(7, len(horas_dia)))

fig2 = go.Figure(data=go.Heatmap(
    z=demanda,
    x=horas_dia,
    y=dias_semana,
    colorscale='Reds',
    hoverongaps=False,
    hovertemplate='Dia: %{y}<br>Hora: %{x}<br>Demanda: %{z} pacientes<extra></extra>'
))

fig2.update_layout(
    height=400,
    xaxis_title="Horário",
    yaxis_title="Dia da Semana",
    yaxis=dict(autorange='reversed')
)

st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Dashboard de KPIs
st.subheader("🎯 Indicadores de Desempenho")

col_kpi1, col_kpi2 = st.columns(2)

with col_kpi1:
    # Gauge - Ocupação das Unidades
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 78,
        title = {'text': "Ocupação das Unidades"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgreen"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig_gauge.update_layout(height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_kpi2:
    # Gráfico de radar - Eficiência por unidade
    categorias = ['Triagem', 'Atendimento', 'Espera', 'Satisfação', 'Recursos']
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=[92, 85, 78, 88, 75],
        theta=categorias,
        fill='toself',
        name='UPA Centro',
        line_color='blue'
    ))
    
    fig_radar.add_trace(go.Scatterpolar(
        r=[85, 88, 82, 85, 80],
        theta=categorias,
        fill='toself',
        name='Hospital Municipal',
        line_color='green'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        height=300
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)

# Tabela de alertas
st.subheader("🚨 Alertas e Notificações")

alertas = pd.DataFrame({
    'Hora': ['14:25', '13:40', '12:15', '11:30', '10:45'],
    'Unidade': ['UPA Zona Norte', 'Hospital Municipal', 'UPA Centro', 'UBS Jardim', 'UPA Centro'],
    'Tipo': ['Capacidade', 'Tempo de Espera', 'Equipamento', 'Pessoal', 'Sistema'],
    'Nível': ['Alto', 'Médio', 'Baixo', 'Médio', 'Crítico'],
    'Status': ['Ativo', 'Resolvido', 'Monitorando', 'Ativo', 'Resolvido'],
    'Descrição': ['90% de ocupação', 'Espera > 60min', 'Raio-X offline', 'Falta de enfermeiro', 'API instável']
})

# Função para colorir nível
def colorir_nivel(val):
    if val == 'Crítico':
        return 'background-color: #EF4444; color: white'
    elif val == 'Alto':
        return 'background-color: #F59E0B; color: white'
    elif val == 'Médio':
        return 'background-color: #FBBF24; color: black'
    else:
        return 'background-color: #10B981; color: white'

st.dataframe(
    alertas.style.applymap(colorir_nivel, subset=['Nível']),
    use_container_width=True,
    hide_index=True
)

# Filtros avançados
with st.expander("🔍 Filtros Avançados de Monitoramento"):
    col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
    
    with col_filtro1:
        periodo = st.select_slider(
            "Período de Análise",
            options=['4 horas', '12 horas', '24 horas', '7 dias', '30 dias'],
            value='12 horas'
        )
    
    with col_filtro2:
        tipo_grafico = st.multiselect(
            "Tipos de Gráfico",
            ['Linha', 'Barra', 'Área', 'Heatmap', 'Radar'],
            default=['Linha', 'Heatmap']
        )
    
    with col_filtro3:
        metrica = st.selectbox(
            "Métrica Principal",
            ['Tempo de Espera', 'Taxa de Ocupação', 'Pacientes Atendidos', 'Eficiência']
        )
    
    if st.button("Aplicar Filtros", type="primary"):
        st.success(f"Filtros aplicados: {periodo}, {', '.join(tipo_grafico)}, {metrica}")
        st.rerun()

# Rodapé informativo
st.divider()
st.caption(f"📡 Dados atualizados em tempo real | Última atualização: {datetime.now().strftime('%H:%M:%S')}")
st.caption("💡 Dica: Clique em qualquer ponto dos gráficos para ver detalhes específicos")
