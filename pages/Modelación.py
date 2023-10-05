import streamlit as st

from time import sleep
from stqdm import stqdm

st.set_page_config(layout='wide')

st.header('Modelación')
st.caption('SimpliCity - Versión Beta 1.0.0')

st.markdown("""
            <style>
            .text-justify {
                text-align: justify;
            }
            </style>
            <div class="text-justify">
            El componente <strong>Escenario</strong> constituye el mecanismo a través del cual se implementan distintos escenarios de modelación y simulación. Contempla la definición del conjunto de parámetros de modelación que se aplican al territorio en cuestión y los valores de variables objetivo (e.g., oferta total de un tipo de uso de suelo en un año determinado) permitiendo explorar diversos futuros posibles y evaluar las consecuencias de diferentes intervenciones urbanas o políticas públicas. Bajo esta configuración, un territorio se compone de un Escenario Base y un conjunto de Escenarios Alternativos.            </div>
            <br>
            <br>
            """, unsafe_allow_html=True)

with st.expander("ESCENARIO BASE"):

    st.markdown("""
            <style>
            .text-justify {
                text-align: justify;
            }
            </style>
            <div class="text-justify">
            <br>
            El <strong>Escenario Base</strong> representa una proyección \textit{ceteris paribus} de los patrones de localización observados de los agentes en el área de estudio, es decir, manteniendo constantes las condiciones actuales. Se configura a partir de: (i) el registro de los agentes localizados en una zonificación específica, y (ii) los planes reguladores comunales, seccionales y/o intercomunales aplicables al área de estudio, que muestran las regulaciones de uso de suelo y constructibilidad que restringen la localización de agentes.            <br>
            <br>
            """, unsafe_allow_html=True)
    
    base_scenario_name = st.text_input('NOMBRE', 'Puerto Varas Base PRC 1990')

    uploaded_file_base = st.file_uploader("NORMATIVA VIGENTE")

    transportation_modes = st.multiselect('MODOS DE TRANSPORTE', ['Automóvil', 'Caminata'])

    col1, col2 = st.columns(2)
    with col1:
        estimation_start_year = st.text_input('AÑO INICIAL DE ESTIMACIÓN', 2010)
    with col2:
        estimation_end_year = st.text_input('AÑO FINAL DE ESTIMACIÓN', 2023)

    col1, col2 = st.columns(2)
    with col1:
        simulation_start_year = st.text_input('AÑO INICIAL DE SIMULACIÓN', 2023)
    with col2:
        simulation_end_year = st.text_input('AÑO FINAL DE SIMULACIÓN', 2050)
    
    col1, col2 = st.columns(2)
    with col1:
        predictors = st.multiselect('AGENTES PREDICTORES', ['Comercial', 'Deportivo', 'Educacional', 'Habitacional', 'Oficina', 'Salud', 'Parcela de Agrado'])
    with col2:
        predictors = st.multiselect('AGENTES A PREDECIR', ['Comercial', 'Deportivo', 'Educacional', 'Habitacional', 'Oficina', 'Salud', 'Parcela de Agrado'])
    
    if st.button(f'SIMULAR ESCENARIO BASE', use_container_width = True):
        for _ in stqdm(range(50)):
            sleep(0.05)
        st.success('¡Genial! Tu Escenario Base "Puerto Varas Base PRC 1990" se ha simulado con éxito. Dirígete a la pestaña "Resultados" para acceder a las visualizaciones y los datos generados a partir de tu reciente simulación. Descubre cómo tu escenario configura el futuro del territorio y examina las diferentes distribuciones espaciales generadas.')

with st.expander("ESCENARIO ALTERNATIVO"):

    st.markdown("""
            <style>
            .text-justify {
                text-align: justify;
            }
            </style>
            <div class="text-justify">
            <br>
            Una vez configurado y simulado el Escenario Base, es necesario identificar el conjunto de opciones que se desean analizar en el horizonte temporal de evaluación, las cuales se estructuran como <strong>Escenarios Alternativos</strong>. Un escenario alternativo se enmarca en el Territorio ya creado, permitiendo la manipulación de dos variables claves: (i) la actualización de las regulaciones aplicables al área de estudio, incluyendo las versiones más recientes o futuras de los planes reguladores, seccionales y/o intercomunales que se deseen evaluar; (ii) la localización de proyectos de infraestructura, como por ejemplo, la construcción de un hospital, la localización de un centro comercial, el desarrollo de proyectos de vivienda social, entre otros y (iii) cambios en la red de transporte, como, por ejemplo, la construcción de un nuevo acceso a la ciudad. Los tres tipos de variables inducen cambios en los criterios de simulación que se aplican. Por tanto, se procede a realizar una simulación alternativa utilizando los modelos estimados previamente, pero considerando estas variables modificadas.            <br>
            <br>
                """, unsafe_allow_html=True)
    
    alternative_scenario_name = st.text_input('NOMBRE', 'Puerto Varas Alternativo PRC 2024')
    
    tab1, tab2, tab3 = st.tabs(['ACTUALIZAR NORMATIVA VIGENTE', 'AGREGAR PROYECTO DE INFRAESTRUCTURA', 'ACTUALIZAR RED DE TRANSPORTE (PRÓXIMAMENTE)'])

    with tab1:
        uploaded_file_alt = st.file_uploader("NORMATIVA PROPUESTA")
    
    with tab2:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            land_use_new_building = st.selectbox('AGENTE', ('Comercial', 'Deportivo', 'Educacional', 'Habitacional', 'Oficina', 'Salud', 'Parcela de Agrado'))
        with col2:
            address_new_building = st.text_input('DIRECCIÓN')
        with col3:
            m2_new_building = st.text_input('METROS CUADRADOS')
        with col4:
            year_new_building = st.text_input('AÑO DE CONSTRUCCIÓN')

    if st.button(f'SIMULAR ESCENARIO ALTERNATIVO', use_container_width = True):
        for _ in stqdm(range(50)):
            sleep(0.05)
        st.success('¡Genial! Tu Escenario Alternativo "Puerto Varas Alternativo PRC 2024" se ha simulado con éxito. Dirígete a la pestaña "Resultados" para acceder a las visualizaciones y los datos generados a partir de tu reciente simulación. Descubre cómo tu escenario configura el futuro del territorio y examina las diferentes distribuciones espaciales generadas.')
