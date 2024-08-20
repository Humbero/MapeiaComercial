
#import das bibliotecas utilizadas no processo
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO


#apresentação da ferramenta/título
st.title('MapeiaComercial')
st.write('Ferramenta para a geração de mapas espacializando as áreas de atuação de vendedores e distribuidores')


# Seleção de estado de carregamento de dados dos usuário

estados = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

# Dicas de apoio ao usuáro e seleção de estado
st.write('### Preenchimento de dados iniciais')

estado_selecionado = st.selectbox('##### Selecione o estado que deseja mapear:',estados)

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

#chamada da função de carga
gdf_selecionado = carga_gdf(estado_selecionado)


#carga de arquivo do tipo excel fornecido pelo usuário
st.subheader("Carregue o arquivo do tipo excel(.xlsx) com suas contribuições:")
excel_carga = st.file_uploader("Escolhar um arquivo excel", type=['xlsx'])

#validação de arquivo
if excel_carga is not None:

    #carregamento do arquivo fornecido pelo usuário
    df_user = pd.read_excel(excel_carga, engine='openpyxl')


    #Tratamento interno de dados------------------------------------------------------------------------------------------------

    #Definindo a coluna CD_NUM como números inteiros para garantir o processo de join
    df_user['CODIBGE'] = df_user['CODIBGE'].astype(int)
    gdf_selecionado['CD_MUN'] =gdf_selecionado['CD_MUN'].astype(int)

    #join utilizando o código do município no IBGE contido na coluna "CD_MUN" como agregador da informação
    gdf_merge = gdf_selecionado.merge(df_user[['CODIBGE','CONSULTOR','DISTRIBUIDOR']], left_on='CD_MUN',right_on='CODIBGE', how='left')

 
    #Plot dos consultores-----------------------------------------------------------------------------------------------------------------------

    # Ajuste o tamanho da figura para A4
    plt.figure(figsize=(841, 11189))

    #plot do estado em branco como base, caso haja espaços vazios o vetor aparecerá normalmente
    ax = gdf_selecionado.plot(color='white', edgecolor='lightgray', linewidth=0.5)

    # Plote o GeoDataFrame com as colunas especificadas e ajuste a legenda
    gdf_merge.plot(column='CONSULTOR', legend=True, ax=ax, edgecolor='lightgray', linewidth=0.5)

    # Ajuste a posição da legenda para que não cubra o mapa e tenha um tamanho = 8
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((1, 0.1))
    leg.set_title('Legenda', prop={'size': 8})
    for text in leg.get_texts():
        text.set_fontsize(8) 

    #adicionando o nome dos municípios ao mapa em fonte de tamanho 2
    for x, y, label in zip(gdf_merge.geometry.centroid.x, gdf_merge.geometry.centroid.y, gdf_merge['NM_MUN']):
        ax.annotate(label, xy=(x, y), fontsize=1, color='black', ha='center')

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
    plt.savefig(buffer, format='jpeg', dpi=800)
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

    #plot do estado em branco como base, caso haja espaços vazios o vetor aparecerá normalmente
    ax = gdf_selecionado.plot(color='white', edgecolor='lightgray', linewidth=0.5)

    # Plote o GeoDataFrame com as colunas especificadas e ajuste a legenda
    gdf_merge.plot(column='DISTRIBUIDOR', legend=True,ax=ax, edgecolor='lightgray', linewidth=0.5)

    # Ajuste a posição da legenda para que não cubra o mapa
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((1, 0.1))
    leg.set_title('Legenda', prop={'size': 8})
    for text in leg.get_texts  ():
        text.set_fontsize(8)

    #adicionando o nome dos municípios ao mapa em fonte de tamanho 2
    for x, y, label in zip(gdf_merge.geometry.centroid.x, gdf_merge.geometry.centroid.y, gdf_merge['NM_MUN']):
        ax.annotate(label, xy=(x, y), fontsize=1, color='black', ha='center')

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
    plt.savefig(buffer, format='jpeg', dpi=800)
    buffer.seek(0)

    # Botão para download do mapa como JPEG
    st.download_button(
        label="Baixar mapa como JPEG",
        data=buffer,
        file_name="mapa_distribuidores.jpeg",
        mime="image/jpeg"
    )
