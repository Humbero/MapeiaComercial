
#import das bibliotecas utilizadas no processo
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px


#tela de apresentação
st.title('Mapas automáticos')
st.write('Este produto gera mapas automáticos para informações dispostas em duas colunas de um arquivo do tipo EXCEL devidamente padronizado.')

#carga de arquivo do tipo excel
st.subheader("Carregue o arquivo EXCEL padronizado com suas contribuições:")
excel_carga = st.file_uploader("Escolhar um arquivo excel", type=['xlsx'])

#validação de arquivo
if excel_carga is not None:
    df_user = pd.read_excel(excel_carga, engine='openpyxl')


#Tratamento interno de dados do usuário------------------------------------------------------------------------------------------------

#caga do arquivos de base referente a geometria do estado de pernambuco
local_geo = 'PE_MUNICIPIOS.geojson'
gdf_PE = gpd.read_file("PE_MUNICIPIOS.geojson")

#Definindo a coluna CD_NUM como números inteiros para garantir o processo de join
df_user['CD_MUN'] = df_user['CD_MUN'].astype(int)
gdf_PE['CD_MUN'] =gdf_PE['CD_MUN'].astype(int)

#join utilizando o código do município no IBGE contido na coluna "CD_MUN" como agregador da informação
gdf_merge = gdf_PE.merge(df_user[['CD_MUN','CONSULTOR','DISTRIBUIDOR']], on='CD_MUN', how='left')


#Plot dos consultores-----------------------------------------------------------------------------------------------------------------------

# Ajuste o tamanho da figura para A4 em polegadas (A4 size: 8.27 x 11.69 inches)
plt.figure(figsize=(841, 11189), tight_layout=True)

# Plote o GeoDataFrame com as colunas especificadas e ajuste a legenda
ax = gdf_merge.plot(column='CONSULTOR', legend=True)

# Ajuste a posição da legenda para que não cubra o mapa
# Por exemplo, coloque a legenda no canto inferior esquerdo com um espaçamento da borda
leg = ax.get_legend()
leg.set_bbox_to_anchor((1, 0.1))
leg.set_title('Legenda', prop={'size': 10})  # Ajuste o tamanho da fonte da legenda

# Remova os valores dos eixos x e y
ax.set_xticks([])
ax.set_yticks([])

# Remova o retângulo em volta do mapa (frame)
ax.set_frame_on(False)

# Exiba o gráfico
st.pyplot(plt)

#plot com plotly express
express_consultores = px.choropleth(gdf_merge,
                                    geojson=gdf_merge.geometry,
                                    locations=gdf_merge.index,
                                    color='CONSULTOR',
                                    projection='mercator',
                                    color_discrete_sequence=px.colors.qualitative.Plotly)

#Ajustando o foco para o plotado
express_consultores .update_geos(
    fitbounds='locations',
    visible=False
)



express_consultores.show()
#Plot dos distribuidores---------------------------------------------------------------------------------------------

# Ajuste o tamanho da figura para A4 em polegadas (A4 size: 8.27 x 11.69 inches)
plt.figure(figsize=(841, 11189), tight_layout=True)

# Plote o GeoDataFrame com as colunas especificadas e ajuste a legenda
ax = gdf_merge.plot(column='DISTRIBUIDOR', legend=True)

# Ajuste a posição da legenda para que não cubra o mapa
# Por exemplo, coloque a legenda no canto inferior esquerdo com um espaçamento da borda
#leg = ax.get_legend()
#leg.set_bbox_to_anchor((1, 0.1))
#leg.set_title('Legenda', prop={'size': 10})  # Ajuste o tamanho da fonte da legenda

# Remova os valores dos eixos x e y
ax.set_xticks([])
ax.set_yticks([])

# Remova o retângulo em volta do mapa (frame)
ax.set_frame_on(False)

plt.legend(fontsize='10')
plt.legend(ncol=2)
plt.legend(bbox_to_anchor=(1,0.1))
# Exiba o gráfico
st.pyplot(plt)


