import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np

from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl

from time import sleep
from stqdm import stqdm


st.set_page_config(layout='wide')



import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)




@st.cache_data
def read_geojson(db_name):
    geojson = gpd.read_file(f'data/{db_name}.geojson') 
    return geojson

def upload_normative():
    uploaded_file = st.file_uploader("SUBE EL PLAN REGULADOR COMUNAL")
    return uploaded_file

def contexto_sociodemografico(censo):
    st.subheader('Contexto Sociodemográfico')

    st.markdown("""
            <style>
            .text-justify {
                text-align: justify;
            }
            </style>
            <div class="text-justify">
            Con el objetivo de contextualizar, se presentan a continuación los datos que permiten caracterizar, en términos generales, a la población de Puerto Varas, a partir del Censo 2017.
            </div>
            <br>
            """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Población", "32.117")
    col2.metric("Hogares", "10.334")
    col3.metric("Viviendas", "11.908")
    col4.metric("Personas por Hogar", "3,11")

    col1, col2 = st.columns(2)
    col1.metric("Proporción Inmigrantes", "8,3%")
    col2.metric("Proporción Adulto Mayor", "1,3%")

    st.markdown('#### Categorización por Tipo de Vivienda')

    casas = int(censo['VIV_CASA'].sum())
    deptos = int(censo['VIV_DEPTO'].sum())
    indigena = int(censo['VIV_IND'].sum())
    pieza = int(censo['VIV_PIEZA'].sum())
    mediagua = int(censo['VIV_MEDIAGUA'].sum())
    movil = int(censo['VIV_MOVIL'].sum())


    col1, col2, col3 = st.columns(3)
    col1.metric("Casas", "10.780")
    col2.metric("Departamentos", deptos)
    col3.metric("Viviendas Tradicional Indígena", indigena)

    col1, col2, col3 = st.columns(3)
    col1.metric("Piezas en Casa Antigua o Conventillo", pieza)
    col2.metric("Mediaguas", mediagua)
    col3.metric("Móviles", movil)

    st.markdown("""
            <style>
            .text-justify {
                text-align: justify;
            }
            </style>
            <br>
            """, unsafe_allow_html=True)
    
def run():   

    st.markdown("""
            <style>
            .text-justify {
                text-align: justify;
            }
            </style>
            <div class="text-justify">
            Puerto Varas se ubica geográficamente en la región de Los Lagos, en el sur de Chile. Específicamente, se encuentra en la ribera oeste del lago Llanquihue. La ciudad está a unos 20 kilómetros al norte de Puerto Montt, la capital de la región, y está bien conectada a través de la carretera Panamericana, que atraviesa todo Chile. En cuanto a su población, según datos del Censo 2017, Puerto Varas tiene una población de alrededor de 40,000 habitantes. La ciudad ha experimentado un crecimiento constante en los últimos años, en parte debido al turismo y a su popularidad como lugar para vivir, en particular entre las personas que buscan un equilibrio entre la vida urbana y el acceso a la naturaleza.
            </div>
            <br>
            <br>
            """, unsafe_allow_html=True)
    
    st.image('https://storage.googleapis.com/chile-travel-newsite-static-content/2021/07/puerto-varas_prin-min.jpg')
    
    censo = read_geojson('CENSUS_DATA')
    censo_updated = read_geojson('CENSUS_DATA_UPDATED')
    campamentos = read_geojson('INFORMAL_SETTLEMENTS')
    normativa = read_geojson('PRC')
    sitios_eriazos = read_geojson('SITIOS_ERIAZOS')

    salud = read_geojson('CENTROS_SALUD')
    salud = salud.to_crs(4326)
    salud['long'] = salud['geometry'].x
    salud['lat'] = salud['geometry'].y
    salud = salud.astype(str)

    educacion_basica = read_geojson('EDUCACION_BASICA')
    educacion_basica = educacion_basica.to_crs(4326)
    educacion_basica['long'] = educacion_basica['geometry'].x
    educacion_basica['lat'] = educacion_basica['geometry'].y
    #educacion_basica = educacion_basica.astype(str)

    educacion_inicial = read_geojson('EDUCACION_INICIAL')
    educacion_inicial = educacion_inicial.to_crs(4326)
    educacion_inicial['long'] = educacion_inicial['geometry'].x
    educacion_inicial['lat'] = educacion_inicial['geometry'].y
    #educacion_inicial = educacion_inicial.astype(str)

    transporte = read_geojson('PARADEROS_TRANSPORTE')
    transporte = transporte.to_crs(4326)
    transporte['long'] = transporte['geometry'].x
    transporte['lat'] = transporte['geometry'].y
    #transporte = transporte.astype(str)

    parques = read_geojson('PARQUES')

    plazas = read_geojson('PLAZAS')

    carabineros = read_geojson('UNIDAD_CARABINEROS')
    carabineros = carabineros.to_crs(4326)
    carabineros['long'] = carabineros['geometry'].x
    carabineros['lat'] = carabineros['geometry'].y
    #carabineros = carabineros.astype(str)

    accs_BPU = pd.read_json('data/DISTANCE_TO_BPU.json')

    st.markdown("""
            <style>
            .text-justify {
                text-align: justify;
            }
            </style>
            <br>
            <br>
            """, unsafe_allow_html=True)

    contexto_sociodemografico(censo = censo)

    st.subheader('Resultados Geográficos')

    st.markdown("""
                <style>
                .text-justify {
                    text-align: justify;
                }
                </style>
                <div class="text-justify">
                A continuación se presentan una serie de cuadros relacionados con distintos temas de interés. Al hacer clic en cada uno de ellos, se desplegará un mapa correspondiente al tema del cuadro seleccionado. Esta interactividad te permitirá explorar y profundizar en las áreas que te resulten más relevantes, proporcionando una experiencia personalizada y dinámica.
                </div>
                <br>
                <br>
                """, unsafe_allow_html=True)

    with st.expander("Densidad de Habitantes por Hectárea"):
        st.subheader("Densidad de Habitantes por Hectárea")

        st.markdown("""
                <style>
                .text-justify {
                    text-align: justify;
                }
                </style>
                <div class="text-justify">
                En el siguiente mapa se presenta la densidad poblacional en Puerto Varas, según los datos del Censo 2017. La densidad está representada por manzana censal, lo que proporciona una visión granular de la distribución de la población en la ciudad.            
                </div>
                <br>
                <br>
                """, unsafe_allow_html=True)

        config_densidad = {'version': 'v1', 'config': {'visState': {'filters': [], 'layers': [{'id': 'pz55g3', 'type': 'geojson', 'config': {'dataId': 'Censo 2017', 'label': 'Censo 2017', 'color': [30, 150, 190], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': [137, 218, 193], 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#FFC300', '#F1920E', '#E3611C', '#C70039', '#900C3F', '#5A1846'], 'reversed': True}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'DENSIDAD', 'type': 'real'}, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}], 'interactionConfig': {'tooltip': {'fieldsToShow': {'Censo 2017': [{'name': 'DENSIDAD', 'format': None}, {'name': 'PERSONAS', 'format': None}, {'name': 'HOGARES', 'format': None}, {'name': 'VIVIENDAS', 'format': None}]}, 'compareMode': False, 'compareType': 'absolute', 'enabled': True}, 'brush': {'size': 0.5, 'enabled': False}, 'geocoder': {'enabled': False}, 'coordinate': {'enabled': False}}, 'layerBlending': 'normal', 'splitMaps': [], 'animationConfig': {'currentTime': None, 'speed': 1}}, 'mapState': {'bearing': 0, 'dragRotate': False, 'latitude': -41.321152076822315, 'longitude': -72.97442591933643, 'pitch': 0, 'zoom': 13.181339693480755, 'isSplit': False}, 'mapStyle': {'styleType': 'satellite', 'topLayerGroups': {}, 'visibleLayerGroups': {}, 'threeDBuildingColor': [3.7245996603793508, 6.518049405663864, 13.036098811327728], 'mapStyles': {}}}}
        map_1 = KeplerGl(config=config_densidad)
        map_1.add_data(data=censo, name='Censo 2017')
        keplergl_static(map_1)

    with st.expander("Hogares Allegados y Campamentos"):

        st.subheader("Hogares Allegados y Campamentos")

        st.markdown("""
                <style>
                .text-justify {
                    text-align: justify;
                }
                </style>
                <div class="text-justify">
                El siguiente mapa ilustra la distribución de los hogares allegados y campamentos en Puerto Varas, basándose en los datos del Censo 2017 y MINVU 2022. Esta visualización proporciona una mirada detallada a la distrubición geográfica del déficit habitacional en cada manzana censal.
                </div>
                <br>
                <br>
                """, unsafe_allow_html=True)
        
        config_deficit = {'version': 'v1', 'config': {'visState': {'filters': [{'dataId': ['Censo 2017'], 'id': 'coxr2x5469', 'name': ['HOG_ALLEG'], 'type': 'range', 'value': [1, 9], 'enlarged': False, 'plotType': 'histogram', 'animationWindow': 'free', 'yAxis': None, 'speed': 1}], 'layers': [{'id': 'aabqwk', 'type': 'geojson', 'config': {'dataId': 'Campamentos', 'label': 'Campamentos', 'color': [255, 248, 51], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': [137, 218, 193], 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': True, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': None, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}, {'id': 'i8vuww', 'type': 'geojson', 'config': {'dataId': 'Censo 2017', 'label': 'Censo 2017', 'color': [130, 154, 227], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': [231, 159, 213], 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#FFC300', '#F1920E', '#E3611C', '#C70039', '#900C3F', '#5A1846'], 'reversed': True}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'HOG_ALLEG', 'type': 'integer'}, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}], 'interactionConfig': {'tooltip': {'fieldsToShow': {'Censo 2017': [{'name': 'HOG_ALLEG', 'format': None}, {'name': 'HOGARES', 'format': None}], 'Campamentos': [{'name': 'OBJECTID', 'format': None}, {'name': 'FOLIO_NUM', 'format': None}, {'name': 'FOLIO', 'format': None}, {'name': 'NOMBRE', 'format': None}, {'name': 'REGION', 'format': None}]}, 'compareMode': False, 'compareType': 'absolute', 'enabled': True}, 'brush': {'size': 0.5, 'enabled': False}, 'geocoder': {'enabled': False}, 'coordinate': {'enabled': False}}, 'layerBlending': 'normal', 'splitMaps': [], 'animationConfig': {'currentTime': None, 'speed': 1}}, 'mapState': {'bearing': 0, 'dragRotate': False, 'latitude': -41.32511749663712, 'longitude': -72.97600216582228, 'pitch': 0, 'zoom': 12.863895028079012, 'isSplit': False}, 'mapStyle': {'styleType': 'satellite', 'topLayerGroups': {}, 'visibleLayerGroups': {}, 'threeDBuildingColor': [3.7245996603793508, 6.518049405663864, 13.036098811327728], 'mapStyles': {}}}}
        map_2 = KeplerGl(config=config_deficit)
        map_2.add_data(data=censo, name='Censo 2017')
        map_2.add_data(data=campamentos, name='Campamentos')
        keplergl_static(map_2)

    with st.expander("Bienes Públicos Urbanos (BPU)"):
        st.subheader("Bienes Públicos Urbanos (BPU)")
        st.markdown("""
                <style>
                .text-justify {
                    text-align: justify;
                }
                </style>
                <div class="text-justify">
                A continuación se presenta la distribución de los Bienes Públicos Urbanos (BPU) en Puerto Varas, según la información recopilada por el SIEDU en 2020. Esta representación permite apreciar la ubicación de estos bienes por manzana censal y su accesibilidad.
                </div>
                <br>
                """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:

            st.markdown("#### Localización de BPU")
            config_equipamiento = {'version': 'v1', 'config': {'visState': {'filters': [], 'layers': [{'id': 'x8i7n35', 'type': 'point', 'config': {'dataId': 'Salud', 'label': 'Salud', 'color': [250, 194, 0], 'highlightColor': [252, 242, 26, 255], 'columns': {'lat': 'lat', 'lng': 'long', 'altitude': None}, 'isVisible': True, 'visConfig': {'radius': 30, 'fixedRadius': False, 'opacity': 0.8, 'outline': False, 'thickness': 0.5, 'strokeColor': None, 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radiusRange': [0, 50], 'filled': True}, 'hidden': False, 'textLabel': []}, 'visualChannels': {'colorField': None, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear'}}, {'id': 'u4qdapx', 'type': 'point', 'config': {'dataId': 'Educación Básica', 'label': 'Educación Básica', 'color': [234, 68, 68], 'highlightColor': [252, 242, 26, 255], 'columns': {'lat': 'lat', 'lng': 'long', 'altitude': None}, 'isVisible': True, 'visConfig': {'radius': 30, 'fixedRadius': False, 'opacity': 0.8, 'outline': False, 'thickness': 0.5, 'strokeColor': None, 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radiusRange': [0, 50], 'filled': True}, 'hidden': False, 'textLabel': [{'field': {'name': 'NOMBRE_RBD', 'type': 'string'}, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': None, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear'}}, {'id': '5slfvvk', 'type': 'point', 'config': {'dataId': 'Educación Inicial', 'label': 'Educación Inicial', 'color': [234, 68, 68], 'highlightColor': [252, 242, 26, 255], 'columns': {'lat': 'lat', 'lng': 'long', 'altitude': None}, 'isVisible': True, 'visConfig': {'radius': 30, 'fixedRadius': False, 'opacity': 0.8, 'outline': False, 'thickness': 0.5, 'strokeColor': None, 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radiusRange': [0, 50], 'filled': True}, 'hidden': False, 'textLabel': [{'field': {'name': 'INST', 'type': 'string'}, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': None, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear'}}, {'id': 'v9dfjj', 'type': 'point', 'config': {'dataId': 'Paraderos de Transporte', 'label': 'Paraderos de Transporte', 'color': [34, 63, 154], 'highlightColor': [252, 242, 26, 255], 'columns': {'lat': 'lat', 'lng': 'long', 'altitude': None}, 'isVisible': True, 'visConfig': {'radius': 30, 'fixedRadius': False, 'opacity': 0.8, 'outline': False, 'thickness': 0.5, 'strokeColor': None, 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radiusRange': [0, 50], 'filled': True}, 'hidden': False, 'textLabel': []}, 'visualChannels': {'colorField': None, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear'}}, {'id': 'd6bo6io', 'type': 'point', 'config': {'dataId': 'Carabineros', 'label': 'Carabineros', 'color': [61, 122, 62], 'highlightColor': [252, 242, 26, 255], 'columns': {'lat': 'lat', 'lng': 'long', 'altitude': None}, 'isVisible': True, 'visConfig': {'radius': 30, 'fixedRadius': False, 'opacity': 0.8, 'outline': False, 'thickness': 0.5, 'strokeColor': None, 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radiusRange': [0, 50], 'filled': True}, 'hidden': False, 'textLabel': [{'field': {'name': 'NOMBRE_UNI', 'type': 'string'}, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': None, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear'}}, {'id': 'am0oegt', 'type': 'geojson', 'config': {'dataId': 'Plazas', 'label': 'Plazas', 'color': [183, 136, 94], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': [246, 209, 138], 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': None, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}, {'id': '2wle5nc', 'type': 'geojson', 'config': {'dataId': 'Parques', 'label': 'Parques', 'color': [173, 185, 51], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': [77, 193, 156], 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': None, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}, {'id': '2bmours', 'type': 'geojson', 'config': {'dataId': 'Censo 2017', 'label': 'Censo 2017', 'color': [166, 165, 165], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.2, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': [130, 154, 227], 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': None, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}], 'interactionConfig': {'tooltip': {'fieldsToShow': {'Censo 2017': [{'name': 'DENSIDAD', 'format': None}, {'name': 'PERSONAS', 'format': None}, {'name': 'HOGARES', 'format': None}, {'name': 'VIVIENDAS', 'format': None}], 'Salud': [{'name': 'NOMBRE', 'format': None}], 'Educación Básica': [{'name': 'NOMBRE_RBD', 'format': None}], 'Educación Inicial': [{'name': 'INST', 'format': None}], 'Paraderos de Transporte': [{'name': 'stop_name', 'format': None}], 'Parques': [{'name': 'NOMBRE_EP', 'format': None}], 'Plazas': [{'name': 'NOMBRE_EP', 'format': None}], 'Carabineros': [{'name': 'NOMBRE_UNI', 'format': None}]}, 'compareMode': False, 'compareType': 'absolute', 'enabled': True}, 'brush': {'size': 0.5, 'enabled': False}, 'geocoder': {'enabled': False}, 'coordinate': {'enabled': False}}, 'layerBlending': 'normal', 'splitMaps': [], 'animationConfig': {'currentTime': None, 'speed': 1}}, 'mapState': {'bearing': 0, 'dragRotate': False, 'latitude': -41.32408351022062, 'longitude': -72.97610432910251, 'pitch': 0, 'zoom': 13.146018090347269, 'isSplit': False}, 'mapStyle': {'styleType': 'satellite', 'topLayerGroups': {}, 'visibleLayerGroups': {}, 'threeDBuildingColor': [3.7245996603793508, 6.518049405663864, 13.036098811327728], 'mapStyles': {}}}}
            map_3 = KeplerGl(config=config_equipamiento)
            map_3.add_data(data=censo, name='Censo 2017')
            map_3.add_data(data=salud, name='Salud')
            map_3.add_data(data=educacion_basica, name='Educación Básica')
            map_3.add_data(data=educacion_inicial, name='Educación Inicial')
            map_3.add_data(data=transporte, name='Paraderos de Transporte')
            map_3.add_data(data=parques, name='Parques')
            map_3.add_data(data=plazas, name='Plazas')
            map_3.add_data(data=carabineros, name='Carabineros')
            keplergl_static(map_3)

        with col2:

            st.markdown("#### Accesibilidad a BPU")
            config_acc_BPU = {'version': 'v1', 'config': {'visState': {'filters': [], 'layers': [{'id': '06bk79i', 'type': 'geojson', 'config': {'dataId': 'Censo 2017', 'label': 'Censo 2017', 'color': [18, 92, 119], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': [77, 193, 156], 'colorRange': {'name': 'Custom Palette', 'type': 'custom', 'category': 'Custom', 'colors': ['#831A3D', '#D55D0E', '#5A1846', '#FFC300', '#AC1C17']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'AVG_CAT_BPU', 'type': 'string'}, 'colorScale': 'ordinal', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}], 'interactionConfig': {'tooltip': {'fieldsToShow': {'Censo 2017': [{'name': 'AVG_CAT_BPU', 'format': None}]}, 'compareMode': False, 'compareType': 'absolute', 'enabled': True}, 'brush': {'size': 0.5, 'enabled': False}, 'geocoder': {'enabled': False}, 'coordinate': {'enabled': False}}, 'layerBlending': 'normal', 'splitMaps': [], 'animationConfig': {'currentTime': None, 'speed': 1}}, 'mapState': {'bearing': 0, 'dragRotate': False, 'latitude': -41.322232909955396, 'longitude': -72.97568523809888, 'pitch': 0, 'zoom': 12.919031451940743, 'isSplit': False}, 'mapStyle': {'styleType': 'satellite', 'topLayerGroups': {}, 'visibleLayerGroups': {}, 'threeDBuildingColor': [3.7245996603793508, 6.518049405663864, 13.036098811327728], 'mapStyles': {}}}}
            map_4 = KeplerGl(config=config_acc_BPU)
            map_4.add_data(data=censo, name='Censo 2017')
            keplergl_static(map_4)

        if st.checkbox('Mostrar Distancia Promedio a BPU'):

            col1, col2 = st.columns(2)

            with col1: 
                st.subheader("Distancia Promedio a BPU")
                st.markdown("""
                <style>
                .text-justify {
                    text-align: justify;
                }
                </style>
                <div class="text-justify">
                Se estima la distancia a la que se encuentran las manzanas censales de cada BPU más cercano en cinco categorías: Muy Cerca, Cerca, Regular, Lejos y Muy Lejos. Siguiendo la metodología del Consejo Nacional de Desarrollo Urbano, estas categorías se determinaron calculando los quintiles de la muestra para las manzanas de Puerto Varas.
                </div>
                <br>
                """, unsafe_allow_html=True)
            with col2:
                st.dataframe(accs_BPU[:7])

    with st.expander("Índice Socio Material y Territorial (ISMT)"):

        st.subheader("Índice Socio Material y Territorial (ISMT)")

        st.markdown("""
                <style>
                .text-justify {
                    text-align: justify;
                }
                </style>
                <div class="text-justify">
                El Índice Socio Material y Territorial (ISMT) busca identificar rasgos y tendencias de la materialidad que den señales territoriales de los componentes de la pobreza y precariedad socioeconómica del hábitat urbano/rural. A continuación se presentan sus resultados georreferenciados por manzana censal para Puerto Varas.
                </div>
                <br>
                """, unsafe_allow_html=True)

        config_ISMT = {'version': 'v1', 'config': {'visState': {'filters': [], 'layers': [{'id': 'ivnhgjd', 'type': 'geojson', 'config': {'dataId': 'Censo 2017', 'label': 'Censo 2017', 'color': [241, 92, 23], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': [34, 63, 154], 'colorRange': {'name': 'ColorBrewer GnBu-6', 'type': 'sequential', 'category': 'ColorBrewer', 'colors': ['#f0f9e8', '#ccebc5', '#a8ddb5', '#7bccc4', '#43a2ca', '#0868ac']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'ISMT_NUMERICAL', 'type': 'integer'}, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}], 'interactionConfig': {'tooltip': {'fieldsToShow': {'Censo 2017': [{'name': 'ISMT', 'format': None}]}, 'compareMode': False, 'compareType': 'absolute', 'enabled': True}, 'brush': {'size': 0.5, 'enabled': False}, 'geocoder': {'enabled': False}, 'coordinate': {'enabled': False}}, 'layerBlending': 'normal', 'splitMaps': [], 'animationConfig': {'currentTime': None, 'speed': 1}}, 'mapState': {'bearing': 0, 'dragRotate': False, 'latitude': -41.32306651793211, 'longitude': -72.97444022058387, 'pitch': 0, 'zoom': 12.675560562557608, 'isSplit': False}, 'mapStyle': {'styleType': 'satellite', 'topLayerGroups': {}, 'visibleLayerGroups': {}, 'threeDBuildingColor': [3.7245996603793508, 6.518049405663864, 13.036098811327728], 'mapStyles': {}}}}
        map_5 = KeplerGl(config=config_ISMT)
        map_5.add_data(data=censo_updated, name='Censo 2017')
        keplergl_static(map_5)

    with st.expander("Prioridad de Inversión Pública"):

        st.subheader("Prioridad de Inversión Pública")

        st.markdown("""
                <style>
                .text-justify {
                    text-align: justify;
                }
                </style>
                <div class="text-justify">
                Se calcula el Índice de Déficit de Ciudad (IDC) del Sistema de Indicadores y Estándares de Desarrollo Urbano (SIEDU) del CNDU, identificando zonas prioritarias de inversión pública, buscando focalizar la inversión en aquellos sectores que tienen bajo nivel de acceso a equipamientos y una alta vulnerabilidad socioeconómica dada por el proxy del ISMT.
                </div>
                <br>
                """, unsafe_allow_html=True)
        
        config_priority = {'version': 'v1', 'config': {'visState': {'filters': [], 'layers': [{'id': 'nu04j1', 'type': 'geojson', 'config': {'dataId': 'Censo 2017', 'label': 'Censo 2017', 'color': [130, 154, 227], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': [231, 159, 213], 'colorRange': {'name': 'ColorBrewer BuPu-3', 'type': 'sequential', 'category': 'ColorBrewer', 'colors': ['#e0ecf4', '#9ebcda', '#8856a7']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'PRIORITY_NUMERICAL', 'type': 'integer'}, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}], 'interactionConfig': {'tooltip': {'fieldsToShow': {'Censo 2017': [{'name': 'PRIORITY', 'format': None}]}, 'compareMode': False, 'compareType': 'absolute', 'enabled': True}, 'brush': {'size': 0.5, 'enabled': False}, 'geocoder': {'enabled': False}, 'coordinate': {'enabled': False}}, 'layerBlending': 'normal', 'splitMaps': [], 'animationConfig': {'currentTime': None, 'speed': 1}}, 'mapState': {'bearing': 0, 'dragRotate': False, 'latitude': -41.32455627114156, 'longitude': -72.97201687247555, 'pitch': 0, 'zoom': 12.651091514072377, 'isSplit': False}, 'mapStyle': {'styleType': 'satellite', 'topLayerGroups': {}, 'visibleLayerGroups': {}, 'threeDBuildingColor': [3.7245996603793508, 6.518049405663864, 13.036098811327728], 'mapStyles': {}}}}
        map_6 = KeplerGl(config=config_priority)
        map_6.add_data(data=censo_updated, name='Censo 2017')
        keplergl_static(map_6)

    with st.expander("Plan Regulador Comunal"):

        st.subheader("Plan Regulador Comunal")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
                <style>
                .text-justify {
                    text-align: justify;
                }
                </style>
                <div class="text-justify">
                Para proceder con el análisis del Plan Regulador de la comuna de Puerto Varas, es necesario que sigas los pasos indicados para subir el archivo correspondiente. Es importante asegurarse de que el Plan Regulador incluya información sobre densidades brutas máximas y una categorización por zonas. Esta información es crucial para la posterior detección de las zonas con potencial de desarrollo habitacional. Una vez que el archivo esté subido correctamente, podrás visualizar el mapa correspondiente en el lado derecho de la pantalla.
                </div>
                <br>
                """, unsafe_allow_html=True)
            gdf = upload_normative()
        
        with col2:
            if gdf != None:
                config_PRC = {'version': 'v1', 'config': {'visState': {'filters': [], 'layers': [{'id': 'r1r8cwp', 'type': 'geojson', 'config': {'dataId': 'Plan Regulador Comunal', 'label': 'Plan Regulador Comunal', 'color': [130, 154, 227], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': [231, 159, 213], 'colorRange': {'name': 'ColorBrewer OrRd-5', 'type': 'sequential', 'category': 'ColorBrewer', 'colors': ['#fef0d9', '#fdcc8a', '#fc8d59', '#e34a33', '#b30000']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'Den_Br_Max', 'type': 'integer'}, 'colorScale': 'quantize', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}], 'interactionConfig': {'tooltip': {'fieldsToShow': {'Plan Regulador Comunal': [{'name': 'Zona_1', 'format': None}, {'name': 'Nombre_1', 'format': None}, {'name': 'Den_Br_Max', 'format': None}, {'name': 'Coe_const', 'format': None}, {'name': 'Coe_ocu_su', 'format': None}]}, 'compareMode': False, 'compareType': 'absolute', 'enabled': True}, 'brush': {'size': 0.5, 'enabled': False}, 'geocoder': {'enabled': False}, 'coordinate': {'enabled': False}}, 'layerBlending': 'normal', 'splitMaps': [], 'animationConfig': {'currentTime': None, 'speed': 1}}, 'mapState': {'bearing': 0, 'dragRotate': False, 'latitude': -41.321103902558995, 'longitude': -72.968637521978, 'pitch': 0, 'zoom': 12.352238227681609, 'isSplit': False}, 'mapStyle': {'styleType': 'satellite', 'topLayerGroups': {}, 'visibleLayerGroups': {}, 'threeDBuildingColor': [3.7245996603793508, 6.518049405663864, 13.036098811327728], 'mapStyles': {}}}}
                map_7 = KeplerGl(config=config_PRC)
                map_7.add_data(data=normativa, name='Plan Regulador Comunal')
                keplergl_static(map_7)

    with st.expander("Potencial de Densificación Habitacional"):

        st.subheader("Potencial de Densificación Habitacional")

        st.markdown("""
                <style>
                .text-justify {
                    text-align: justify;
                }
                </style>
                <div class="text-justify">
                El siguiente apartado presenta el análisis del Potencial de Densificación Habitacional de Puerto Varas. Este análisis se realizó considerando dos insumos principales: la densidad de población de acuerdo al Censo 2017, y la densidad máxima permitida por la zonificación del Plan Regulador Comunal (PRC) adjunto, que hace referencia a una propuesta actualización de 2022. En este contexto, se exploró la accesibilidad a bienes públicos urbanos de cada manzana, permitiendo evaluar el potencial de desarrollo habitacional en la comuna.
                </div>
                <br>
                """, unsafe_allow_html=True)
        
        config_pot_dens_hab = {'version': 'v1', 'config': {'visState': {'filters': [], 'layers': [{'id': '9ylu8b', 'type': 'geojson', 'config': {'dataId': 'Censo 2017', 'label': 'Censo 2017', 'color': [241, 92, 23], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': [34, 63, 154], 'colorRange': {'name': 'Custom Palette', 'type': 'custom', 'category': 'Custom', 'colors': ['#FED98E', '#FE9929', '#CC4C02', '#FFFFD4']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'POT_DENS_HAB_NUMERICAL', 'type': 'string'}, 'colorScale': 'ordinal', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}], 'interactionConfig': {'tooltip': {'fieldsToShow': {'Censo 2017': [{'name': 'POT_DENS_HAB', 'format': None}]}, 'compareMode': False, 'compareType': 'absolute', 'enabled': True}, 'brush': {'size': 0.5, 'enabled': False}, 'geocoder': {'enabled': False}, 'coordinate': {'enabled': False}}, 'layerBlending': 'normal', 'splitMaps': [], 'animationConfig': {'currentTime': None, 'speed': 1}}, 'mapState': {'bearing': 0, 'dragRotate': False, 'latitude': -41.32595634458889, 'longitude': -72.97212566787704, 'pitch': 0, 'zoom': 12.875426485949061, 'isSplit': False}, 'mapStyle': {'styleType': 'satellite', 'topLayerGroups': {}, 'visibleLayerGroups': {}, 'threeDBuildingColor': [3.7245996603793508, 6.518049405663864, 13.036098811327728], 'mapStyles': {}}}}
        map_8 = KeplerGl(config=config_pot_dens_hab)
        map_8.add_data(data=censo_updated, name='Censo 2017')
        keplergl_static(map_8)

    with st.expander("Accesibilidad a Bienes Públicos Urbanos y Potencial Habitacional"):

        st.subheader("Accesibilidad a Bienes Públicos Urbanos y Potencial Habitacional")

        st.markdown("""
                <style>
                .text-justify {
                    text-align: justify;
                }
                </style>
                <div class="text-justify">
                A continuación, se muestran dos mapas. El primer mapa muestra la Accesibilidad a Bienes Públicos Urbanos y el Potencial Habitacional, resaltando los Sitios Eriazos según datos obtenidos del Servicio de Impuestos Internos (SII) de Chile. El segundo mapa superpone la ubicación de los sitios eriazos en un mapa base que representa el Valor del Suelo según áreas homogéneas, también proporcionadas por el SII.
                </div>
                <br>
                """, unsafe_allow_html=True)
        
        col1, col2 =st.columns(2)

        with col1:

            st.markdown("#### Sitios Eriazos")
            config_sitio_eriazo = {'version': 'v1', 'config': {'visState': {'filters': [], 'layers': [{'id': 'c4claf5', 'type': 'geojson', 'config': {'dataId': 'Campamentos', 'label': 'Campamentos', 'color': [32, 17, 99], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': None, 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': None, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}, {'id': 'jqon33q', 'type': 'geojson', 'config': {'dataId': 'Sitios Eriazos', 'label': 'Sitios Eriazos', 'color': [246, 209, 138], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 2, 'strokeColor': None, 'colorRange': {'name': 'ColorBrewer OrRd-6', 'type': 'sequential', 'category': 'ColorBrewer', 'colors': ['#fef0d9', '#fdd49e', '#fdbb84', '#fc8d59', '#e34a33', '#b30000']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'SUP_PREDIAL', 'type': 'integer'}, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}, {'id': 'o8f64yl', 'type': 'geojson', 'config': {'dataId': 'Censo 2017', 'label': 'Censo 2017', 'color': [248, 149, 112], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': [130, 154, 227], 'colorRange': {'name': 'Custom Palette', 'type': 'custom', 'category': 'Custom', 'colors': ['#018571', '#80CDC1', '#A6611A', '#DFC27D', '#F5F5F5']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'BPU_POT_HAB', 'type': 'string'}, 'colorScale': 'ordinal', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}], 'interactionConfig': {'tooltip': {'fieldsToShow': {'Censo 2017': [{'name': 'BPU_POT_HAB', 'format': None}, {'name': 'AVG_CAT_BPU', 'format': None}, {'name': 'ISMT', 'format': None}, {'name': 'PRIORITY', 'format': None}, {'name': 'POT_DENS_HAB', 'format': None}], 'Sitios Eriazos': [{'name': 'PREDIO', 'format': None}, {'name': 'SUP_PREDIAL', 'format': None}, {'name': 'VALOR_PREDIAL', 'format': None}], 'Campamentos': [{'name': 'NOMBRE', 'format': None}]}, 'compareMode': False, 'compareType': 'absolute', 'enabled': True}, 'brush': {'size': 0.5, 'enabled': False}, 'geocoder': {'enabled': False}, 'coordinate': {'enabled': False}}, 'layerBlending': 'normal', 'splitMaps': [], 'animationConfig': {'currentTime': None, 'speed': 1}}, 'mapState': {'bearing': 0, 'dragRotate': False, 'latitude': -41.322643001747174, 'longitude': -72.97435599506375, 'pitch': 0, 'zoom': 13.049923492499529, 'isSplit': False}, 'mapStyle': {'styleType': 'satellite', 'topLayerGroups': {}, 'visibleLayerGroups': {}, 'threeDBuildingColor': [3.7245996603793508, 6.518049405663864, 13.036098811327728], 'mapStyles': {}}}}
            map_10 = KeplerGl(config = config_sitio_eriazo)
            map_10.add_data(data=censo_updated, name='Censo 2017')
            map_10.add_data(data=sitios_eriazos, name='Sitios Eriazos')
            map_10.add_data(data=campamentos, name='Campamentos')
            keplergl_static(map_10)

        with col2:
            st.markdown("#### Valor del Suelo")
            config_hz = {'version': 'v1', 'config': {'visState': {'filters': [], 'layers': [{'id': 'c4claf5', 'type': 'geojson', 'config': {'dataId': 'Campamentos', 'label': 'Campamentos', 'color': [32, 17, 99], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': None, 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': None, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}, {'id': 'jqon33q', 'type': 'geojson', 'config': {'dataId': 'Sitios Eriazos', 'label': 'Sitios Eriazos', 'color': [246, 209, 138], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 2, 'strokeColor': None, 'colorRange': {'name': 'ColorBrewer OrRd-6', 'type': 'sequential', 'category': 'ColorBrewer', 'colors': ['#fef0d9', '#fdd49e', '#fdbb84', '#fc8d59', '#e34a33', '#b30000']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'SUP_PREDIAL', 'type': 'integer'}, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}, {'id': 'o8f64yl', 'type': 'geojson', 'config': {'dataId': 'Censo 2017', 'label': 'Censo 2017', 'color': [248, 149, 112], 'highlightColor': [252, 242, 26, 255], 'columns': {'geojson': 'geometry'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': [130, 154, 227], 'colorRange': {'name': 'ColorBrewer YlGnBu-5', 'type': 'sequential', 'category': 'ColorBrewer', 'colors': ['#ffffcc', '#a1dab4', '#41b6c4', '#2c7fb8', '#253494']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'enableElevationZoomFactor': True, 'stroked': False, 'filled': True, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'VALOR_BASE', 'type': 'real'}, 'colorScale': 'quantile', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}], 'interactionConfig': {'tooltip': {'fieldsToShow': {'Censo 2017': [{'name': 'BPU_POT_HAB', 'format': None}, {'name': 'AVG_CAT_BPU', 'format': None}, {'name': 'ISMT', 'format': None}, {'name': 'PRIORITY', 'format': None}, {'name': 'POT_DENS_HAB', 'format': None}, {'name': 'VALOR_BASE', 'format': None}], 'Sitios Eriazos': [{'name': 'PREDIO', 'format': None}, {'name': 'SUP_PREDIAL', 'format': None}, {'name': 'VALOR_PREDIAL', 'format': None}], 'Campamentos': [{'name': 'NOMBRE', 'format': None}]}, 'compareMode': False, 'compareType': 'absolute', 'enabled': True}, 'brush': {'size': 0.5, 'enabled': False}, 'geocoder': {'enabled': False}, 'coordinate': {'enabled': False}}, 'layerBlending': 'normal', 'splitMaps': [], 'animationConfig': {'currentTime': None, 'speed': 1}}, 'mapState': {'bearing': 0, 'dragRotate': False, 'latitude': -41.322643001747174, 'longitude': -72.97435599506375, 'pitch': 0, 'zoom': 13.049923492499529, 'isSplit': False}, 'mapStyle': {'styleType': 'satellite', 'topLayerGroups': {}, 'visibleLayerGroups': {}, 'threeDBuildingColor': [3.7245996603793508, 6.518049405663864, 13.036098811327728], 'mapStyles': {}}}}
            map_11 = KeplerGl(config = config_hz)
            map_11.add_data(data=censo_updated, name='Censo 2017')
            map_11.add_data(data=sitios_eriazos, name='Sitios Eriazos')
            map_11.add_data(data=campamentos, name='Campamentos')
            keplergl_static(map_11)

    st.image('logos/logos.png')

st.header('¡Bienvenido a SimpliCity!')
st.caption('Versión Beta 1.0.0')

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
                <p style="text-align: justify;">En SimpliCity, te ofrecemos un enfoque pr&aacute;ctico y basado en datos para entender y planificar el futuro de los espacios urbanos y territoriales.</p>
    <p style="text-align: justify;"><strong>&iquest;Por qu&eacute; SimpliCity?</strong></p>
    <ol>
        <li style="text-align: justify;"><strong>Modela y Proyecta:</strong> Utiliza nuestras herramientas para evaluar el impacto de diversas pol&iacute;ticas urbanas, a trav&eacute;s del uso de tecnolog&iacute;a de vanguardia, algoritmos avanzados y modelos econom&eacute;tricos.</li>
        <li style="text-align: justify;"><strong>Explora y Descubre:</strong> Aprovecha las visualizaciones interactivas que te permiten navegar por los escenarios futuros de desarrollo urbano y territorial.</li>
        <li style="text-align: justify;"><strong>Compara y Decide:</strong> La toma de decisiones se vuelve m&aacute;s sencilla con nuestras herramientas intuitivas y un conjunto de datos comprehensivo. Compara estrategias, eval&uacute;a escenarios alternativos y opta por el mejor camino.</li>
    </ol>
    <p style="text-align: justify;">Con SimpliCity, accedes a una plataforma robusta que te permite no solo analizar, sino tambi&eacute;n interactuar y dar forma a los posibles escenarios futuros de tu territorio. Ya sea que est&eacute;s evaluando pol&iacute;ticas existentes o imaginando nuevos horizontes para tu regi&oacute;n, nuestra plataforma est&aacute; dise&ntilde;ada para darte un control integral y una visi&oacute;n de futuro.</p>
                <br>
                <br>
                """, unsafe_allow_html=True)
    
with col3:
    authenticator.login('Login', 'main')

    if st.session_state["authentication_status"]:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f'Bienvenido, *{st.session_state["name"]}*')
        with col2:
            authenticator.logout('Logout', 'main', key='unique_key')

        territory = st.selectbox(
        'TERRITORIO',
        ('Puerto Montt', 'Puerto Varas'))


    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
    
#st.image('https://storage.googleapis.com/chile-travel-newsite-static-content/2021/07/puerto-varas_prin-min.jpg')
