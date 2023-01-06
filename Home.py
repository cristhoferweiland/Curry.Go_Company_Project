import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon='🎲'
)

#image_path = 'C:/Users/Cweiland/repos/ftc_analise_dados_python/project_course/pages/'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=150 )
st.sidebar.markdown( '### Go Curry or nothing' )
st.sidebar.markdown( '''---''' )

st.sidebar.markdown('# Marketplace App')
st.sidebar.markdown('##### Powered by: Cristhofer Weiland ')
st.sidebar.markdown('##### 2022 @ Comunidade DS ')

st.write( '## CURRY.GO - Dashboard de Crescimento' )

url = "https://www.linkedin.com/in/cristhoferweiland/"

st.markdown(
    """
    O Dashboard de Crescimento da CURRY.GO foi elaborado para acompanhar métricas através da perspectiva da Empresa, dos Entregadores e dos Restaurantes.
    ### Como utilizar este Dashboard?
    - Visão Empresa
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores de Crescimento por semana.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador
        - Visão Gerencial: Métricas gerais.
        - Avaliações: por entregador, por trânsito e por clima.
        - Entregas: entregadores mais rápidos e mais lentos.
    - Visão Restaurante
        - Visão Geral: Métricas de comportamento.
        - Distribuição por Distância
        - Distribuição por Tempo
    ### Precisa de Ajuda?
    - E-mail: crisweiland@gmail.com
""")
st.markdown("- Acesse meu [LinkedIn](%s)." % url)