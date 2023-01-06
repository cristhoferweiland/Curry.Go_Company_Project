# ============================================================
# Bibliotecas
# ============================================================
import pandas as pd
import streamlit as st
import plotly.express as px
from haversine import haversine
import folium
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Empresa', page_icon='📊', layout='wide')

# ============================================================
# Funções
# ============================================================

def clean_code( df ):
    """ Esta função tem a responsabilidade de limpar o DataFrame
        
        Tipos de Limpeza:
        1. Remoção dos espaços das variáveis texto
        2. Remoção dos dados com linhas vazias (NaN)
        3. Converção do tipo de variável
        4. Limpeza da coluna de tempo (remoção do texto da variável)
        
        Input: DataFrame
        Output: DataFrame"""
    # 1. REMOVENDO espaços dentro das strings
    df.loc[:, 'ID'] = df.loc[:, 'ID'].str.strip()
    df.loc[:, 'Road_traffic_density'] = df.loc[:, 'Road_traffic_density'].str.strip()
    df.loc[:, 'Delivery_person_ID'] = df.loc[:, 'Delivery_person_ID'].str.strip()
    df.loc[:, 'Type_of_order'] = df.loc[:,'Type_of_order'].str.strip()
    df.loc[:, 'Type_of_vehicle'] = df.loc[:,'Type_of_vehicle'].str.strip()
    df.loc[:, 'City'] = df.loc[:,'City'].str.strip()
    df.loc[:, 'Festival'] = df.loc[:,'Festival'].str.strip()

    # 2. EXCLUINDO LINHAS VAZIAS das colunas DELIVERY_PERSON_AGE e MULTIPLE_DELIVERIES
    # (Conceito de seleção Condicional)
    linhas_vazias = df['Delivery_person_Age'] != 'NaN '
    df = df.loc[linhas_vazias, :].copy()
    linhas_vazias = df['multiple_deliveries'] != 'NaN '
    df = df.loc[linhas_vazias, :].copy()
    linhas_vazias = df['City'] != 'NaN'
    df = df.loc[linhas_vazias, :].copy()
    linhas_vazias = df['Festival'] != 'NaN '
    df = df.loc[linhas_vazias, :].copy()
    linhas_vazias = df['Road_traffic_density'] != 'NaN'
    df = df.loc[linhas_vazias, :].copy()

    # 3. CONVERTENDO os tipos das variáveis para utilização
    df['Delivery_person_Age'] = df['Delivery_person_Age'].astype( int )
    df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype( float )
    df['Order_Date'] = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )
    df['multiple_deliveries'] = df['multiple_deliveries'].astype( int )

    # 4. Removendo a sujeira da coluna Time_taken(min)
    df['Time_taken(min)'] = df['Time_taken(min)'].apply( lambda x: x.split( '(min) ' )[1] )
    df['Time_taken(min)'] = df['Time_taken(min)'].astype( int )
    
    return df


def pedidos_por_dia( df ):
    # colunas
    cols = ['ID', 'Order_Date']
    # agrupando as colunas
    df_aux = df.loc[:, cols].groupby('Order_Date').count().reset_index()
    # desenhar o gráfico de linhas (biblioteca plotly)
    fig = px.bar( df_aux, x='Order_Date', y="ID")
    
    return fig


def percent_pedidos_trafego( df ):
    df_aux = df.loc[:, ['ID', 'Road_traffic_density']].groupby( 'Road_traffic_density' ).count().reset_index()
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    #fazendo um gráfico de pizza
    fig = px.pie( df_aux, values= 'entregas_perc', names='Road_traffic_density')
    
    return fig


def pedidos_cidade_trafego( df ):
    df_aux = ( df.loc[:, ['ID', 'City', 'Road_traffic_density']]
                 .groupby( ['City','Road_traffic_density'] )
                 .count()
                 .reset_index() )
    fig = px.scatter( df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    
    return fig


def pedidos_por_semana( df ):
    df['week_of_year'] = df["Order_Date"].dt.strftime( '%U' )
    df_aux = df.loc[: , ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    df_aux.head()
    fig = px.line( df_aux, x='week_of_year', y='ID' )
        
    return fig


def pedidos_entregador_semana( df ):
    # quantidade de pedidos por semana / número único de entregadores por semana
    df_aux01 = df.loc[: , ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux02 = ( df.loc[: , ['Delivery_person_ID', 'week_of_year']]
                   .groupby('week_of_year')
                   .nunique()
                   .reset_index() )
    # juntando dois dataframes
    df_aux = pd.merge( df_aux01, df_aux02, how='inner')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')
        
    return fig


def mapa_local( df ):
    df_aux = ( df.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                 .groupby(['City', 'Road_traffic_density'])
                 .median()
                 .reset_index() )

    map_ = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']], 
                        popup=location_info[['City', 'Road_traffic_density']]).add_to(map_)
    folium_static(map_, width=800, height=600)
    
    return None # pois já retorna um mapa
              

# --------------------------------------- INÍCIO DA ESTRUTURA LÓGICA DO CÓDIGO -----------------------------------------

# ============================================================
# Importando o dataset
# ============================================================

df_raw = pd.read_csv('dataset/train.csv')


# ============================================================
# Limpeza do dados
# ============================================================

df = clean_code( df_raw )


# ============================================================
# Barra Lateral
# ============================================================

#image_path = 'C:/Users/Cweiland/repos/ftc_analise_dados_python/project_course/pages/'
image = Image.open( 'logo.png' )
st.sidebar.image(image, width=120)


st.sidebar.markdown('''---''')
st.sidebar.markdown('## Filtros:')
#st.sidebar.markdown('''---''')


date_slider = st.sidebar.slider(
'Selecione uma data limite:', value=pd.datetime(2022, 4, 13), min_value=pd.datetime(2022, 2, 11),
max_value=pd.datetime(2022, 4, 6),
format='DD-MM-YYYY')

#st.sidebar.markdown('''---''')

traffic_options = st.sidebar.multiselect(
    ' Quais as condições de trânsito?',
    ['Low', 'Medium', 'High', 'Jam'], default=['Low', 'Medium','High', 'Jam'])

st.sidebar.markdown('''---''')
st.sidebar.markdown('# Marketplace App')
st.sidebar.markdown('##### Powered by: Cristhofer Weiland ')
st.sidebar.markdown('##### 2022 @ Comunidade DS ')

# Fazendo os filtros funcionarem
# Filtro de Data
linhas_selecionadas = df['Order_Date'] < date_slider
df = df.loc[linhas_selecionadas, :]

# Filtro de trânsito
linhas_selecionadas = df['Road_traffic_density'].isin(traffic_options)
df = df.loc[linhas_selecionadas, :]


# ============================================================
# Layout no Streamlit
# ============================================================

st.header('Marketplace - Visão Empresa')

# Criando as tabs
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        st.markdown('### Pedidos por Dia')
        fig = pedidos_por_dia( df )
        st.plotly_chart(fig, use_container_width=True)
         
    with st.container():
        col1, col2 = st.columns( 2 )
        with col1:
            st.markdown( '### Distribuição dos pedidos por tráfego')
            fig = percent_pedidos_trafego( df )
            st.plotly_chart( fig, use_container_width=True)
        
        with col2:
            st.markdown( '### Volume de pedidos por cidade e tráfego')
            fig = pedidos_cidade_trafego( df )
            st.plotly_chart( fig, use_container_width=True)            
    
with tab2:
    with st.container():
        st.markdown('### Pedidos por Semana')
        fig = pedidos_por_semana( df )
        st.plotly_chart( fig, use_container_width=True)        
    
    with st.container():
        st.markdown('### Pedidos por Entregador por Semana')
        fig = pedidos_entregador_semana( df )
        st.plotly_chart(fig, use_container_width=True)
        
        

with tab3:
    st.markdown( '### Mapa de localização por Tráfego ')
    mapa_local( df )
    

    