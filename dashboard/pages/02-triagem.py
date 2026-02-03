import streamlit as st
import pandas as pd
import plotly.express as px
import json
from datetime import datetime
import time

st.set_page_config(
    page_title="Triagem Inteligente",
    page_icon="⚕️",
    layout="wide"
)

st.title("⚕️ Triagem Inteligente com IA")
st.markdown("### Sistema de classificação automática e análise preditiva")

# Barra lateral para simulação de triagem
with st.sidebar:
    st.header("🧪 Simulador de Triagem")
    
    st.subheader("Sintomas do Paciente")
    
    sintomas = st.multiselect(
        "Selecione os sintomas principais:",
        ['Febre', 'Dor de cabeça', 'Tosse', 'Falta de ar', 'Dor no peito',
         'Dor abdominal', 'Náusea/Vômito', 'Tontura', 'Dor nas costas',
         'Sangramento', 'Inchaço', 'Visão turva', 'Palpitações',
         'Confusão mental', 'Convulsão', 'Trauma recente'],
        default=['Febre', 'Tosse']
    )
    
    intensidade = st.slider("Intensidade da dor (0-10):", 0, 10, 5)
    
    idade = st.number_input("Idade:", min_value=0, max_value=120, value=35)
    
    historico = st.text_area("Histórico adicional:", "Paciente relata cansaço e perda de apetite há 3 dias.")
    
    comorbidades = st.multiselect(
        "Comorbidades conhecidas:",
        ['Hipertensão', 'Diabetes', 'Problemas cardíacos', 'Asma',
         'Obesidade', 'Gestante', 'Idoso > 65', 'Nenhuma'],
        default=['Nenhuma']
    )
    
    if st.button("🔍 Executar Triagem com IA", type="primary", use_container_width=True):
        with st.spinner("Analisando com IA..."):
            time.sleep(1.5)
            st.success("Triagem concluída!")
            
            # Simulação de resultado
            prioridades = {
                'emergencia': ['Dor no peito', 'Falta de ar', 'Convulsão', 'Sangramento intenso'],
                'urgente': ['Febre alta', 'Dor abdominal intensa', 'Trauma', 'Vômito persistente'],
                'prioritario': ['Febre moderada', 'Dor moderada', 'Tosse persistente'],
                'eletivo': ['Dor leve', 'Consulta de rotina']
            }
            
            # Lógica simples de priorização
            if any(s in sintomas for s in prioridades['emergencia']) or intensidade >= 9:
                st.error("🚨 **EMERGÊNCIA** - Atendimento imediato necessário")
                st.info("Recomendação: Encaminhar para emergência mais próxima")
            elif any(s in sintomas for s in prioridades['urgente']) or intensidade >= 7:
                st.warning("⚠️ **URGENTE** - Atendimento em até 1 hora")
                st.info("Recomendação: UPA ou ambulatório de urgência")
            elif any(s in sintomas for s in prioridades['prioritario']):
                st.info("📋 **PRIORITÁRIO** - Atendimento em até 4 horas")
                st.info("Recomendação: Unidade básica de saúde com prioridade")
            else:
                st.success("✅ **ELETIVO** - Agendamento regular")
                st.info("Recomendação: Agendar consulta na UBS")
    
    st.divider()
    
    st.subheader("📊 Estatísticas da IA")
    st.metric("Precisão", "94.2%", "+0.8%")
    st.metric("Triagens Hoje", "342", "+28")
    st.metric("Tempo Médio", "12s", "-3s")

# Conteúdo principal
tab1, tab2, tab3 = st.tabs(["📈 Análise de Tendências", "🤖 Modelos de IA", "🎯 Histórico de Casos"])

with tab1:
    st.header("Análise de Tendências de Sintomas")
    
    # Dados simulados
    semanas = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4']
    sintomas_trend = pd.DataFrame({
        'Semana': semanas * 5,
        'Sintoma': ['Febre']*4 + ['Tosse']*4 + ['Dor Abdominal']*4 + ['Dor de Cabeça']*4 + ['Falta de Ar']*4,
        'Casos': [45, 48, 52, 55, 38, 42, 45, 48, 25, 28, 32, 30, 32, 35, 38, 40, 12, 15, 18, 20]
    })
    
    fig_trend = px.line(
        sintomas_trend,
        x='Semana',
        y='Casos',
        color='Sintoma',
        markers=True,
        title="Evolução Semanal de Sintomas",
        height=500
    )
    
    fig_trend.update_layout(
        hovermode='x unified',
        xaxis_title="Semana",
        yaxis_title="Número de Casos"
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Heatmap de correlação
    st.subheader("🔥 Correlação entre Sintomas e Comorbidades")
    
    correlacao = pd.DataFrame({
        'Hipertensão': [0.8, 0.3, 0.2, 0.1, 0.7],
        'Diabetes': [0.4, 0.6, 0.3, 0.2, 0.5],
        'Cardíacos': [0.2, 0.1, 0.8, 0.3, 0.9],
        'Respiratórios': [0.3, 0.9, 0.2, 0.4, 0.6],
        'Obesidade': [0.5, 0.4, 0.6, 0.3, 0.4]
    }, index=['Febre', 'Tosse', 'Dor Peito', 'Falta Ar', 'Cansaço'])
    
    fig_corr = px.imshow(
        correlacao,
        text_auto='.2f',
        aspect='auto',
        color_continuous_scale='RdBu',
        title="Matriz de Correlação"
    )
    
    st.plotly_chart(fig_corr, use_container_width=True)

with tab2:
    st.header("Modelos de Inteligência Artificial")
    
    col_model1, col_model2 = st.columns(2)
    
    with col_model1:
        st.subheader("🧠 BERT Multilingual")
        st.markdown("""
        **Função:** Análise de texto em triagem
        
        **Especificações:**
        - Base: BERT-base-multilingual-cased
        - Parâmetros: 110M
        - Idiomas: 104 (incluindo Português)
        - Acurácia: 91.3%
        
        **Aplicações:**
        - Classificação de sintomas
        - Análise de histórico médico
        - Detecção de urgência no texto
        """)
        
        if st.button("🔄 Treinar Modelo", key="train_bert"):
            with st.spinner("Treinando modelo BERT..."):
                time.sleep(2)
                st.success("Modelo treinado com sucesso!")
    
    with col_model2:
        st.subheader("📊 XGBoost Classifier")
        st.markdown("""
        **Função:** Classificação de prioridades
        
        **Especificações:**
        - Algoritmo: Gradient Boosting
        - Features: 42 variáveis clínicas
        - Acurácia: 94.2%
        - Recall (emergência): 96.8%
        
        **Características:**
        - Explicabilidade SHAP
        - Baixa latência (< 50ms)
        - Atualização incremental
        """)
        
        if st.button("📈 Ver Explicabilidade", key="explain_xgb"):
            with st.expander("Explicação do Modelo"):
                st.image("https://raw.githubusercontent.com/slundberg/shap/master/docs/artwork/shap_visualization.png", 
                        caption="Explicação SHAP - Importância das Features")
    
    st.divider()
    
    st.subheader("📋 Comparativo de Modelos")
    
    modelos_comparativo = pd.DataFrame({
        'Modelo': ['BERT + XGBoost', 'Random Forest', 'SVM', 'Redes Neurais', 'Regressão Logística'],
        'Acurácia': [94.2, 89.5, 87.2, 91.8, 85.4],
        'Latência (ms)': [120, 45, 180, 320, 25],
        'Explicabilidade': ['Alta', 'Alta', 'Média', 'Baixa', 'Alta'],
        'Treinamento (h)': [6.5, 1.2, 3.8, 12.5, 0.8]
    })
    
    st.dataframe(
        modelos_comparativo.style.highlight_max(subset=['Acurácia'], color='lightgreen')
                               .highlight_min(subset=['Latência (ms)'], color='lightblue'),
        use_container_width=True,
        hide_index=True
    )

with tab3:
    st.header("Histórico de Casos e Aprendizado")
    
    # Filtros para histórico
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        data_inicio = st.date_input("Data Início", datetime.now() - timedelta(days=30))
    
    with col_filter2:
        data_fim = st.date_input("Data Fim", datetime.now())
    
    with col_filter3:
        prioridade_filtro = st.multiselect(
            "Prioridade",
            ['Emergência', 'Urgente', 'Prioritário', 'Eletivo'],
            default=['Emergência', 'Urgente']
        )
    
    # Tabela de casos históricos
    casos_historicos = pd.DataFrame({
        'Data': pd.date_range(start='2024-01-01', periods=20, freq='D'),
        'Paciente': [f'PAC{1000+i}' for i in range(20)],
        'Idade': np.random.randint(18, 80, 20),
        'Sintomas': ['Febre+Tosse', 'Dor abdominal', 'Dor peito', 'Tontura'] * 5,
        'IA_Prioridade': ['Urgente', 'Emergência', 'Emergência', 'Prioritário'] * 5,
        'Médico_Prioridade': ['Urgente', 'Emergência', 'Emergência', 'Prioritário'] * 5,
        'Acerto': ['✅', '✅', '✅', '❌'] * 5
    })
    
    st.dataframe(
        casos_historicos,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Acerto": st.column_config.TextColumn(
                "Acerto IA",
                help="✅ = Acerto | ❌ = Erro"
            )
        }
    )
    
    # Estatísticas de acerto
    st.subheader("📈 Desempenho da IA ao Longo do Tempo")
    
    performance_data = pd.DataFrame({
        'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
        'Acurácia': [88.5, 90.2, 91.8, 92.5, 93.4, 94.2],
        'Recall Emergência': [92.3, 93.1, 94.5, 95.2, 95.8, 96.8],
        'Precisão': [87.8, 89.2, 90.5, 91.3, 92.1, 93.0]
    })
    
    fig_performance = px.line(
        performance_data,
        x='Mês',
        y=['Acurácia', 'Recall Emergência', 'Precisão'],
        markers=True,
        title="Evolução do Desempenho da IA"
    )
    
    fig_performance.update_layout(
        yaxis_title="Porcentagem (%)",
        yaxis_range=[85, 100],
        height=400
    )
    
    st.plotly_chart(fig_performance, use_container_width=True)
    
    # Botão para exportar dados
    if st.button("📤 Exportar Dados de Treinamento"):
        st.success("Dados exportados para formato CSV")
        st.download_button(
            label="⬇️ Baixar CSV",
            data=casos_historicos.to_csv(index=False).encode('utf-8'),
            file_name="dados_treinamento_ia.csv",
            mime="text/csv"
        )

# Informações finais
st.divider()
st.info("""
💡 **Sobre o Sistema de Triagem Inteligente:**
- Baseado em modelos BERT para análise de texto e XGBoost para classificação
- Aprendizado contínuo com novos casos
- Explicabilidade completa das decisões
- Integração com prontuário eletrônico
- Conformidade com LGPD e regulamentações de saúde
""")
