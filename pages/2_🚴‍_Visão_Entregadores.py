# ============================================================
# Bibliotecas
# ============================================================
import pandas as pd
import numpy as np
import plotly.express as px
from haversine import haversine
import folium
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Entregadores', page_icon='🚴‍♂️', layout='wide')

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


def top_entregadores( df, top_asc ):
    # Agrupar pela média das entregas de cada entregador
    df_aux = ( df.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                .groupby( ['City', 'Delivery_person_ID'] )
                .mean().sort_values( ['City','Time_taken(min)'], ascending=top_asc ).reset_index() )

    df_aux01 = df_aux.loc[df_aux['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df_aux.loc[df_aux['City'] == 'Urban', :].head(10)
    df_aux03 = df_aux.loc[df_aux['City'] == 'Semi-Urban', :].head(10)

    df_top = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index( drop=True)
            
    return df_top

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

st.header('Marketplace - Visão Entregadores')

# Criando as tabs
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Avaliações', 'Entregas'])

with tab1:
    with st.container():
        st.markdown('## Métricas gerais')
        st.markdown(' ')
        st.markdown('##### Entregadores')
        col1, col2, col3, col4, col5 = st.columns( 5, gap='small')
        with col1:
            # A maior idade dos entregadores
            max_idade = df.loc[:, 'Delivery_person_Age'].max()
            col1.metric( 'Maior idade', max_idade, 'anos')
        with col2:
            # A menor idade dos entregadores
            min_idade = df.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor idade', min_idade, 'anos')
        with col3:
            # A média da idade dos entregadores
            avg_idade = np.round(df.loc[:, 'Delivery_person_Age'].mean(),1)
            col3.metric('Média de Idade', avg_idade, 'anos')
    
    with st.container():
        st.markdown(' ')
        st.markdown('##### Veículos')
        col1, col2, col3, col4, col5 = st.columns( 5, gap='small')
        with col1:
            # A melhor condição dos veículos
            melhor_cond = df.loc[:, 'Vehicle_condition'].max()
            col1.metric('Melhor cond. Veículo', melhor_cond)
        with col2:
            #A pior condição dos veículos
            pior_cond = df.loc[:, 'Vehicle_condition'].min()
            col2.metric('Pior cond. Veículo', pior_cond)

    
with tab2:
    with st.container():        
        #st.markdown('## Avaliações')
        
        col1, col2, col3 = st.columns( 3 )
        
        with col1:
            st.markdown( '##### Avaliação Média por Entregador')
            df_avg_ratings_per_deliver = ( df.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']]
                                             .groupby('Delivery_person_ID')
                                             .mean()
                                             .reset_index() )
            st.dataframe( df_avg_ratings_per_deliver )
        
        with col2:
            st.markdown( '##### Avaliação Média por Trânsito' )
            df_avg_std_rating_by_traffic = ( df.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                               .groupby( 'Road_traffic_density')
                                               .agg( {'Delivery_person_Ratings': ['mean', 'std' ]} ) )
            # mudanca de nome das colunas
            df_avg_std_rating_by_traffic.columns = ['Média', 'Desvio Padrão']
            # reset do index
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
            st.dataframe( df_avg_std_rating_by_traffic )            
        
        with col3:
            st.markdown( '##### Avaliação Média por Clima')
            # agregando as duas medidas pela função agg
            df_avg_std_rating_by_weather = ( df.loc[:, ['Delivery_person_Ratings','Weatherconditions']]
                                               .groupby('Weatherconditions')
                                               .agg( {'Delivery_person_Ratings' : ['mean', 'std']}) )
            # renomeando as colunas
            df_avg_std_rating_by_weather.columns= ['Média', 'Desvio Padrão']
            # reset do index
            df_avg_std_rating_by_weather = df_avg_std_rating_by_weather.reset_index()
            st.dataframe( df_avg_std_rating_by_weather )

with tab3:        
    with st.container():
        st.markdown('## Velocidade de Entrega')
        
        col1, col2 = st.columns( 2 )
        
        with col1:
            st.markdown ('##### Top Entregadores mais rápidos')
            top_entrega = top_entregadores( df, top_asc=True )
            st.dataframe( top_entrega )
        
        with col2:
            st.markdown( '##### Top Entregadores mais lentos')
            top_entrega = top_entregadores( df, top_asc=False )
            st.dataframe( top_entrega )
            