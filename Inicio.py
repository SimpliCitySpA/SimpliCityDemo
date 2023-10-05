import streamlit as st

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
