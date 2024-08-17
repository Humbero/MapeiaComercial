
#import das bibliotecas utilizadas no processo
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO


#tela de apresentação
st.title('Mapas automáticos')
st.write('Este produto gera mapas automáticos para informações dispostas em duas colunas de um arquivo do tipo EXCEL devidamente padronizado.')


# Pré carregamento de elementos
# Seleção da região de interesse
estados = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

# colinha de apoio a seleção e caixa de seleção para o usuário
st.write('**Colinhas de ajuda com as siglas dos estados** ')
st.write('**Região norte:** Acre (AC), Amapá (AP), Amazonas (AM), Pará (PA), Rondônia (RO), Roraima (RR) e Tocantins (TO)')
st.write('**Região nordeste:** Maranhão (MA), Piauí (PI), Ceará (CE), Rio Grande do Norte (RN), Paraíba (PB), Pernambuco (PE), Alagoas (AL), Sergipe (SE) e Bahia (BA)')
st.write('**Região centro-oeste:** Distrito Federal (DF). Os estados são: Goiás (GO), Mato Grosso (MT) e Mato Grosso do Sul (MS)')
st.write('**Região sudeste:** São Paulo (SP), Rio de Janeiro (RJ), Minas Gerais (MG) e Espírito Santo (ES)')
st.write('**Região sul:** Paraná (PR), Santa Catarina (SC) e Rio Grande do Sul (RS)')

estado_selecionado = st.selectbox('Selecione o estado que deseja mapear:',estados)

#carga do gpk correpondente ao estado selecionado, bem como, corte do estado de interesse
#função para carga do arquivo e filtro por estado tendo como entrada apenas a sigla do estado
def carga_gdf(estado):

    norte = ['AC','AP','AM','PA','RO','RR','TO']
    nordeste = ['MA','PI','CE','RN','PB','PE','AL','SE','BA']
    centro_oeste = ['DF','GO','MT','MS']
    sudeste = ['SP','RJ','MG','ES']
    sul = ['PR','SC','RS']
    
    
    if estado in norte:

        gdf = gpd.read_file('MUNI_NORTE.gpkg')

        gdf_retorno = gdf[gdf['SIGLA_UF'] == estado]
        return(gdf_retorno)

    elif estado in nordeste:
        
        gdf = gpd.read_file('MUNI_NORDESTE.gpkg')

        gdf_retorno = gdf[gdf['SIGLA_UF'] == estado]
        return(gdf_retorno)
        
    elif estado in centro_oeste:
        
        gdf = gpd.read_file('MUNI_CENTRO-OESTE.gpkg')

        gdf_retorno = gdf[gdf['SIGLA_UF'] == estado]
        return(gdf_retorno)
    
    elif estado in sudeste:
            
        gdf = gpd.read_file('MUNI_SUDESTE.gpkg')

        gdf_retorno = gdf[gdf['SIGLA_UF'] == estado]
        return(gdf_retorno)
    
    elif estado in sul:
                
        gdf = gpd.read_file('MUNI_SUL.gpkg')

        gdf_retorno = gdf[gdf['SIGLA_UF'] == estado]
        return(gdf_retorno)

#chamada da função 
gdf_selecionado = carga_gdf(estado_selecionado)


#carga de arquivo do tipo excel
st.subheader("Carregue o arquivo EXCEL padronizado com suas contribuições:")
excel_carga = st.file_uploader("Escolhar um arquivo excel", type=['xlsx'])

#validação de arquivo
if excel_carga is not None:
    df_user = pd.read_excel(excel_carga, engine='openpyxl')


    #Tratamento interno de dados do usuário------------------------------------------------------------------------------------------------

    #Definindo a coluna CD_NUM como números inteiros para garantir o processo de join
    df_user['CD_MUN'] = df_user['CD_MUN'].astype(int)
    gdf_selecionado['CD_MUN'] =gdf_selecionado['CD_MUN'].astype(int)

    #join utilizando o código do município no IBGE contido na coluna "CD_MUN" como agregador da informação
    gdf_merge = gdf_selecionado.merge(df_user[['CD_MUN','CONSULTOR','DISTRIBUIDOR']], on='CD_MUN', how='left')


    #Plot dos consultores-----------------------------------------------------------------------------------------------------------------------

    # Ajuste o tamanho da figura para A4 em polegadas (A4 size: 8.27 x 11.69 inches)
    plt.figure(figsize=(841, 11189))

    # Plote o GeoDataFrame com as colunas especificadas e ajuste a legenda
    ax = gdf_merge.plot(column='CONSULTOR', legend=True, edgecolor='lightgray', linewidth=0.5)

    # Ajuste a posição da legenda para que não cubra o mapa
    # Por exemplo, coloque a legenda no canto inferior esquerdo com um espaçamento da borda
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((1, 0.1))
    leg.set_title('Legenda', prop={'size': 8})
    for text in leg.get_texts():
        text.set_fontsize(8) 

    # Remova os valores dos eixos x e y
    ax.set_xticks([])
    ax.set_yticks([])

    # Remova o retângulo em volta do mapa (frame)
    ax.set_frame_on(False)

    #Titulo provisório
    st.write('Área de atuação dos consultores')
    # Exiba o gráfico
    st.pyplot(plt)

   # Salvar a figura em um buffer de memória para permitir o download
    buffer = BytesIO()
    plt.savefig(buffer, format='jpeg', dpi=600)
    buffer.seek(0)

    # Botão para download do mapa como JPEG
    st.download_button(
        label="Baixar mapa como JPEG",
        data=buffer,
        file_name="mapa_consultores.jpeg",
        mime="image/jpeg"
    )

    #Plot dos distribuidores-----------------------------------------------------------------------------------------------------------------------

    # Ajuste o tamanho da figura para A4 em polegadas (A4 size: 8.27 x 11.69 inches)
    plt.figure(figsize=(841, 11189))

    # Plote o GeoDataFrame com as colunas especificadas e ajuste a legenda
    ax = gdf_merge.plot(column='DISTRIBUIDOR', legend=True, edgecolor='lightgray', linewidth=0.5)

    # Ajuste a posição da legenda para que não cubra o mapa
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((1, 0.1))
    leg.set_title('Legenda', prop={'size': 8})
    for text in leg.get_texts  ():
        text.set_fontsize(8)

    # Remova os valores dos eixos x e y
    ax.set_xticks([])
    ax.set_yticks([])

    # Remova o retângulo em volta do mapa (frame)
    ax.set_frame_on(False)

   
    # Titulo provisório
    st.write('Área de atuação dos distribuidores')
    # Exiba o gráfico
    st.pyplot(plt)

   # Salvar a figura em um buffer de memória para permitir o download
    buffer = BytesIO()
    plt.savefig(buffer, format='jpeg', dpi=600)
    buffer.seek(0)

    # Botão para download do mapa como JPEG
    st.download_button(
        label="Baixar mapa como JPEG",
        data=buffer,
        file_name="mapa_distribuidores.jpeg",
        mime="image/jpeg"
    )