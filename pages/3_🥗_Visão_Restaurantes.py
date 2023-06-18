# ============================================================
# Bibliotecas
# ============================================================
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from haversine import haversine
import datetime from datetime
import folium
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Restaurantes', page_icon='🥗', layout='wide')

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


def distancia( df ):
    cols = ['Restaurant_latitude', 'Restaurant_longitude', 
            'Delivery_location_latitude', 'Delivery_location_longitude']
    df['distance'] = ( df.loc[:, cols].apply( lambda x: 
                                    haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                               (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1) )

    avg_distance = np.round( df['distance'].mean(), 2)
    return avg_distance


def avg_std_time_delivery(df, festival, op):
    """Esta função calcula o tempo médio e o desvio padrão do tempo de entrega.
    Parâmetros:
        Input:
            - df: dataframe com os dados 
            - op: tipo de operação para o cálculo
                'avg_time': calcula o tempo médio
                'std_time': calcula o desvio padrão do tempo.
            - festival: 'yes' ou 'não'
        Output:
            - df: dataframe com 2 colunas e 1 linha."""    
            
    df_aux = ( df.loc[:, ['Time_taken(min)', 'Festival']]
                 .groupby( 'Festival' )
                 .agg( {'Time_taken(min)': ['mean', 'std']} ) )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round( df_aux.loc[df_aux['Festival'] == festival, op], 2 )
                                      
    return df_aux
    

def avg_std_time_graph( df ):
    df_aux = df.loc[:, ['City', 'Time_taken(min)']].groupby( 'City' ).agg( {'Time_taken(min)': ['mean', 'std']} )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
        
    fig = go.Figure() 
    fig.add_trace( go.Bar( name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time']))) 
    fig.update_layout(barmode='group')
    return fig    


def avg_std_time_on_traffic( df ):
    df_aux = ( df.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']]
                 .groupby( ['City', 'Road_traffic_density'] )
                 .agg( {'Time_taken(min)': ['mean', 'std']} ) )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                              color='std_time', color_continuous_scale='RdBu_r',
                              color_continuous_midpoint=np.average(df_aux['std_time'] ) )
    return fig


# --------------------------------------- INÍCIO DA ESTRUTURA LÓGICA DO CÓDIGO -----------------------------------------

# ============================================================
# Importando o dataset
# ============================================================

df_raw = pd.read_csv('dataset/train.csv')


# ============================================================
# Limpeza dos dados
# ============================================================

df = clean_code( df_raw )


# ============================================================
# Barra Lateral
# ============================================================

image = Image.open( 'logo.png' )
st.sidebar.image(image, width=120)

st.sidebar.markdown('''---''')
st.sidebar.markdown('## Filtros:')

date_slider = st.sidebar.slider(
'Selecione uma data limite:', 
    value = datetime.strptime(pd.to_datetime('2022/4/13').strftime('%Y-%m-%d'), '%Y-%m-%d'),
    min_value = datetime.strptime(pd.to_datetime('2022/2/11').strftime('%Y-%m-%d'), '%Y-%m-%d'),
    max_value = datetime.strptime(pd.to_datetime('2022/4/6').strftime('%Y-%m-%d'), '%Y-%m-%d'),format='DD-MM-YYYY')
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

st.header('Marketplace - Visão Restaurantes')

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Distrib. Distância', 'Distrib. Tempo'] )

with tab1:
    with st.container():
        st.markdown('### Métricas gerais')
        col1, col2, col3, col4 = st.columns( 4 )
        
        with col1:
            delivery_unique = len( df.loc[:, 'Delivery_person_ID'].unique() )
            col1.metric( 'Entregadores únicos', delivery_unique)

        with col2:
            avg_distance = distancia( df )
            col2.metric('Distância Média (KM)', avg_distance )
            
        with col3:
            # Tempo médio
            df_aux = avg_std_time_delivery( df, 'No', 'avg_time')
            col3.metric( 'Tempo Médio (min)', df_aux)
            # Tempo médio no festival
            df_aux = avg_std_time_delivery( df, 'Yes', 'avg_time')
            col3.metric( 'Tempo Médio (min)', df_aux, 'Festival' )
            
        with col4:
            # Desvio Padrão
            df_aux = avg_std_time_delivery( df, 'No', 'std_time' )
            col4.metric( 'Desvio Padrão', df_aux )
            # Desvio Padrão no Festival
            df_aux = avg_std_time_delivery( df, 'Yes', 'std_time' )
            col4.metric( 'Desvio Padrão', df_aux, 'Festival' )

    with st.container():
        st.markdown('''---''')
        st.markdown('##### Tempo Médio e Desvio Padrão de Entrega por Cidade')
        fig = avg_std_time_graph( df )
        st.plotly_chart( fig )

            
with tab2:        
    with st.container():
        st.markdown('##### Distância média (em KM) entre os restaurantes e os locais de entrega por cidade')
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
        df['distance'] = df.loc[:, cols].apply( lambda x: 
                                    haversine(  (x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1 )

        avg_distance = df.loc[:, ['City', 'distance']].groupby( 'City' ).mean().reset_index()
        fig = go.Figure( data=[ go.Pie( labels=avg_distance['City'], values=avg_distance['distance'], pull=[0.05, 0.05, 0.05])])
        st.plotly_chart( fig )

with tab3:
    with st.container():
        st.markdown('##### Tempo médio e Desvio Padrão de entrega por cidade e por tipo de tráfego')
        
        fig = avg_std_time_on_traffic( df )
        st.plotly_chart( fig )
            
        
    with st.container():
        st.markdown('''---''')
        st.markdown('##### Tempo médio e Desvio Padrão de entrega por cidade e por tipo de pedido')     

        df_aux = ( df.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']]
                     .groupby( ['City', 'Type_of_order'] )
                     .agg( {'Time_taken(min)': ['mean', 'std']} ) )

        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        st.dataframe( df_aux )
