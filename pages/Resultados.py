import streamlit as st

st.set_page_config(layout='wide')

st.header('Resultados')
st.caption('SimpliCity - Versión Beta 1.0.0')

st.markdown("""
            <style>
            .text-justify {
                text-align: justify;
            }
            </style>
            <div class="text-justify">
            La pestaña <strong>Resultados</strong> no solo te ofrece visualizaciones estáticas, sino que también permite interactuar con los datos para que puedas profundizar en las áreas de interés. Utiliza las herramientas disponibles para filtrar, ordenar y examinar de cerca las variables y métricas clave.            <br>
            <br>
            """, unsafe_allow_html=True)

tab_names1 = ['METROS CUADRADOS HABITACIONAL PEQUEÑO', 
            'METROS CUADRADOS HABITACIONAL MEDIO', 
            'METROS CUADRADOS HABITACIONAL GRANDE', 
            'METROS CUADRADOS HABITACIONALES',
            'TOTAL DE PARCELAS DE AGRADO', 
            'TOTAL DE COMERCIOS']

tab_names = ['HABITACIONAL', 
            'PARCELA DE AGRADO', 
            'COMERCIO']

utility_files = ["Base Scenario/Utility Functions/H1.html",
            "Base Scenario/Utility Functions/H2.html",
            "Base Scenario/Utility Functions/H3.html",
            "Base Scenario/Utility Functions/K.html",
            "Base Scenario/Utility Functions/C.html"]

st.warning('Para asegurar un desempeño fluido y eficaz de los mapas y visualizaciones, recomendamos encarecidamente abrir y explorar una pestaña a la vez. Abrir múltiples pestañas simultáneamente podría comprometer la carga y visualización correcta de los mapas.', icon="⚠️")

selected_tab = st.selectbox("ESCOGE UN AGENTE", tab_names)

if selected_tab == 'HABITACIONAL':
    col1, col2 = st.columns(2)

    with col1: 
        st.session_state.desagg = st.checkbox('¿Desagregar?')

    with col2:
        if st.session_state.desagg:
            agent = st.radio(
                "AGENTE HABITACIONAL",
                ["Pequeño", "Mediano", "Grande"])
            if agent == 'Pequeño':
                st.name = 'METROS CUADRADOS HABITACIONAL PEQUEÑO'
            elif agent == 'Mediano':
                st.name = 'METROS CUADRADOS HABITACIONAL MEDIO'
            elif agent == 'Grande':
                st.name = 'METROS CUADRADOS HABITACIONAL GRANDE'
        else:
            st.name = 'METROS CUADRADOS HABITACIONALES'

elif selected_tab == 'PARCELA DE AGRADO':
    st.name = 'TOTAL DE PARCELAS DE AGRADO'

elif selected_tab == 'COMERCIO':
    st.name = 'TOTAL DE COMERCIOS'

st.session_state.tab_index = tab_names1.index(st.name)

st.divider()

#tab_index = tab_names.index(selected_tab)
st.subheader(st.name)
st.subheader(" ")

if st.session_state.desagg == True:
    with st.expander("FUNCIONES DE UTILIDAD"):
        with open(utility_files[st.session_state.tab_index], "r", encoding="utf-8") as f:
            html_content = f.read()
        st.components.v1.html(html_content, width=None, height=300, scrolling=True)

with st.expander("RESULTADOS POR ESCENARIO"):
    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
            <style>
            .text-justify {
                text-align: justify;
            }
            </style>
            <div class="text-justify">
            <br>
            <strong>Puerto Varas Base PRC 1990</strong>
            <br>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <style>
            .text-justify {
                text-align: justify;
            }
            </style>
            <div class="text-justify">
            <br>
            A continuación, se presenta un mapa interactivo que permite comparar los metros cuadrados y/o total del agente seleccionado entre los años 2023 (izquierda) y 2050 (derecha), bajo la aplicación del Plan Regulador vigente de 1990.
            <br>
                    <br>
            """, unsafe_allow_html=True)
        
        map_files1 = ["Base Maps/H1 2050 PRC.html",
                "Base Maps/H2 2050 PRC.html",
                "Base Maps/H3 2050 PRC.html",
                "Base Maps/H 2050 PRC.html",
                "Base Maps/K 2050 PRC.html",
                "Base Maps/C 2050 PRC.html"]
        
        with open(map_files1[st.session_state.tab_index], "r", encoding="utf-8") as f:
            html_content = f.read()
        st.components.v1.html(html_content, width=None, height=700, scrolling=True)

    with col2:

        st.markdown("""
            <style>
            .text-justify {
                text-align: justify;
            }
            </style>
            <div class="text-justify">
            <br>
            <strong>Puerto Varas Alternativo PRC 2024</strong>
            <br>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <style>
            .text-justify {
                text-align: justify;
            }
            </style>
            <div class="text-justify">
            <br>
            A continuación, se presenta un mapa interactivo que permite comparar los metros cuadrados y/o total del agente seleccionado entre los años 2023 (izquierda) y 2050 (derecha), bajo la aplicación del Plan Regulador propuesto de 2024.
            <br>
                    <br>
            """, unsafe_allow_html=True)
        
        map_files2 = ["Alternative Maps/H1 2050 PRC.html",
                "Alternative Maps/H2 2050 PRC.html",
                "Alternative Maps/H3 2050 PRC.html",
                "Alternative Maps/H 2050 PRC.html",
                "Alternative Maps/K 2050 PRC.html",
                "Alternative Maps/C 2050 PRC.html"]

        with open(map_files2[st.session_state.tab_index], "r", encoding="utf-8") as f:
            html_content = f.read()
        st.components.v1.html(html_content, width=None, height=700, scrolling=True)

with st.expander("COMPARATIVA DE ESCENARIOS"):

    st.markdown("""
        <style>
        .text-justify {
            text-align: justify;
        }
        </style>
        <div class="text-justify">
        <br>
        Esta sección ha sido diseñada para facilitar la comparación entre el Escenario Base (izquierda) y el Alternativo (derecha), proyectados hasta el año 2050, proporcionando una plataforma efectiva para evaluar el impacto de sus propuestas de desarrollo. Su utilidad radica en poder contrastar directamente los posibles futuros y discernir las diferencias clave y los beneficios potenciales de su planificación estratégica.
        <br>
                <br>
        """, unsafe_allow_html=True)
        
    map_files3 = ["maps/H1 2050 PRC.html",
                "maps/H2 2050 PRC.html",
                "maps/H3 2050 PRC.html",
                "maps/H 2050 PRC.html",
                "maps/K 2050 PRC.html",
                "maps/C 2050 PRC.html"]


    with open(map_files3[st.session_state.tab_index], "r", encoding="utf-8") as f:
        html_content = f.read()

    st.components.v1.html(html_content, width=None, height=700, scrolling=False)