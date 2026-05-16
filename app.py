import streamlit as st
import plotly.graph_objects as go
from utils import formatar_moeda
from calculos import calcular_tempo, calcular_aporte, simular_crescimento


# Configuração da página
st.set_page_config(
    page_title='investment calculator',
    page_icon="📈"
)


# Cabeçalho da aplicação
st.title('Investment Calculator')
st.write('💰 Simule o crescimento do seu patrimônio.')


# Coleta de dados
st.divider()

st.subheader('Dados')

col1, col2 = st.columns([1,3])

with col1:
    # Tipo de cálculo
    tipo_calculo = st.selectbox(
        'Calcular:',
        ['Tempo', 'Aporte']
    )


if tipo_calculo == 'Tempo':
    col1, col2 = st.columns([1,1])

    with col1:
        valor_futuro = st.number_input('Valor Final Desejado', min_value=0.0)
        aporte_inicial = st.number_input('Aporte Inicial', min_value=0.0)
    with col2:
        aporte_mensal = st.number_input('Aporte Mensal', min_value=0.0)
        taxa_juros = st.number_input('Taxa de Juros (em %)', min_value=0.1) / 100

if tipo_calculo == 'Aporte':
    col1, col2 = st.columns([1,1])

    with col1:
        valor_futuro = st.number_input('Valor Final Desejado', min_value=0.0)
        aporte_inicial = st.number_input('Aporte Inicial', min_value=0.0)
    with col2:
        tempo_meses = st.number_input('Tempo (em meses)', min_value=1, step=1)
        taxa_juros = st.number_input('Taxa de Juros (em %)', min_value=0.1) / 100


col1, col2, col3 = st.columns([2,1,2])

with col2:
    calcular = st.button('Calcular', use_container_width=True)


# Processamento dos cálculos
resultado = None
erro = False

if calcular:
    if valor_futuro <= aporte_inicial:
        st.error('O valor futuro deve ser maior que o aporte inicial.')
        erro = True

    if tipo_calculo == 'Tempo':

        if aporte_mensal <= 0:
            st.error('O aporte mensal deve ser maior que 0.')
            erro = True


    if not erro:
        if tipo_calculo == 'Tempo':
            tempo_meses = calcular_tempo(valor_futuro, aporte_inicial, aporte_mensal, taxa_juros)
            resultado = simular_crescimento(aporte_inicial, aporte_mensal, taxa_juros, tempo_meses)

        if tipo_calculo == 'Aporte':
            aporte_mensal = calcular_aporte(valor_futuro, aporte_inicial, taxa_juros, tempo_meses)
            resultado = simular_crescimento(aporte_inicial, aporte_mensal, taxa_juros, tempo_meses)



# Exibição dos resultados
st.divider()

st.subheader('Resultado')

if resultado is not None:
    if tipo_calculo == 'Tempo':
        col1, col2 = st.columns([1,1])

        with col1:
            st.metric(
                    'Tempo necessário',
                    f'{tempo_meses} meses'
                )
        with col2:
            st.metric(
                'Patrimônio Final',
                formatar_moeda(resultado[-1]['patrimonio'])
            )

    if tipo_calculo == 'Aporte':
        col1, col2 = st.columns([1,1])

        with col1:
            st.metric(
                'Aporte Necessário',
                formatar_moeda(aporte_mensal)
            )
        with col2:
            st.metric(
                'Patrimônio Final',
                formatar_moeda(resultado[-1]['patrimonio'])
            )
        
    meses = [item['mes'] for item in resultado]
    patrimonios = [item['patrimonio'] for item in resultado]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=meses,
            y=patrimonios,
            mode='lines',
            fill='tozeroy',
            line=dict(
                width=3,
                color='#2196F3'
            ),
            fillcolor='rgba(33, 150, 243, 0.2)'
        )
    )
    fig.update_layout(
        title='Evolução Patrimonial',
        xaxis_title='Meses',
        yaxis_title='Patrimônio',
        template='plotly_dark',
        hovermode='x unified',
        

        height=500,

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),

        xaxis=dict(
            showspikes=True,
            spikedash='solid',
            spikecolor='rgba(255,255,255,0.3)',
            spikesnap='cursor',
            spikethickness=1
        ),

        yaxis=dict(
            showgrid=True
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            'displayModeBar': True,
            'modeBarButtonsToRemove': [
                'zoom',
                'pan',
                'select',
                'lasso2d',
                'zoomIn',
                'zoomOut',
                'autoScale',
                'resetScale'
            ]
        }
    )