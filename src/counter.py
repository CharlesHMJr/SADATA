# %%
#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import folium

from folium.plugins import HeatMap
from geopy.geocoders import Nominatim

# %%
#creates a geolocator to locate the birth places and work places
geolocator = Nominatim(user_agent="103962022")

#creates a list to store the birth places coordinates and the work places coordinates
coordenadasNascimento = []
coordenadasAtuacao = []

# %%
#count the education
contHistoricos = pd.read_csv('./results/primary/historicos.csv', sep=',')

#count the education based on start
contHistoricosInicio = contHistoricos.value_counts(['CURSO-TECNICO-PROFISSIONALIZANTE', 'Início.1'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()
contHistoricosInicio = pd.concat([contHistoricosInicio, contHistoricos.value_counts(['GRADUACAO', 'Início.2'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()], axis=1)
contHistoricosInicio = pd.concat([contHistoricosInicio, contHistoricos.value_counts(['MESTRADO', 'Início.4'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()], axis=1)
contHistoricosInicio = pd.concat([contHistoricosInicio, contHistoricos.value_counts(['DOUTORADO', 'Início.5'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()], axis=1)
#create a csv file with the data
contHistoricosInicio.to_csv('./results/quantitative/contHistoricosInicio.csv', sep=',', encoding='utf-8', index=False)

#count the education based on end
contHistoricosFim = contHistoricos.value_counts(['CURSO-TECNICO-PROFISSIONALIZANTE', 'Fim.1']).to_frame('Quantidade').reset_index()
contHistoricosFim = pd.concat([contHistoricosFim, contHistoricos.value_counts(['GRADUACAO', 'Fim.2']).to_frame('Quantidade').reset_index()], axis=1)
contHistoricosFim = pd.concat([contHistoricosFim, contHistoricos.value_counts(['MESTRADO', 'Fim.4']).to_frame('Quantidade').reset_index()], axis=1)
contHistoricosFim = pd.concat([contHistoricosFim, contHistoricos.value_counts(['DOUTORADO', 'Fim.5']).to_frame('Quantidade').reset_index()], axis=1)
#create a csv file with the data
contHistoricosFim.to_csv('./results/quantitative/contHistoricosFim.csv', sep=',', encoding='utf-8', index=False)

#count the education in the university
contHistoricosUni = pd.read_csv('./results/primary/historicosUniversidade.csv', sep=',')

#count the education in the university based on start
contHistoricosUniInicio = contHistoricosUni.value_counts(['CURSO-TECNICO-PROFISSIONALIZANTE', 'Início.1'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()
contHistoricosUniInicio = pd.concat([contHistoricosUniInicio, contHistoricosUni.value_counts(['GRADUACAO', 'Início.2'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()], axis=1)
contHistoricosUniInicio = pd.concat([contHistoricosUniInicio, contHistoricosUni.value_counts(['MESTRADO', 'Início.4'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()], axis=1)
contHistoricosUniInicio = pd.concat([contHistoricosUniInicio, contHistoricosUni.value_counts(['DOUTORADO', 'Início.5'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()], axis=1)
#create a csv file with the data
contHistoricosUniInicio.to_csv('./results/quantitative/contHistoricosUniInicio.csv', sep=',', encoding='utf-8', index=False)

#count the education in the university based on end
contHistoricosUniFim = contHistoricosUni.value_counts(['CURSO-TECNICO-PROFISSIONALIZANTE', 'Fim.1']).to_frame('Quantidade').reset_index()
contHistoricosUniFim = pd.concat([contHistoricosUniFim, contHistoricosUni.value_counts(['GRADUACAO', 'Fim.2']).to_frame('Quantidade').reset_index()], axis=1)
contHistoricosUniFim = pd.concat([contHistoricosUniFim, contHistoricosUni.value_counts(['MESTRADO', 'Fim.4']).to_frame('Quantidade').reset_index()], axis=1)
contHistoricosUniFim = pd.concat([contHistoricosUniFim, contHistoricosUni.value_counts(['DOUTORADO', 'Fim.5']).to_frame('Quantidade').reset_index()], axis=1)
#create a csv file with the data
contHistoricosUniFim.to_csv('./results/quantitative/contHistoricosUniFim.csv', sep=',', encoding='utf-8', index=False)
# %%
#get the birth places and work places
localizacao = pd.read_csv('./results/primary/localizacao.csv', sep=',')

#count the birth places
contNascimento = localizacao.value_counts(['Cidade de Origem', 'Estado de Origem']).to_frame('Quantidade')
contNascimento.to_csv('./csv/contNascimento.csv', sep=',', encoding='utf-8')

#count the work places
contAtuacao = localizacao.value_counts(['Cidade de Atuação', 'Estado de Atuação']).to_frame('Quantidade')
contAtuacao.to_csv('./results/quantitative/contAtuacao.csv', sep=',', encoding='utf-8')

# %%
#locate the birth places coordinates and register their occurrences number
for local in contNascimento.index:
    try:
        print(local)
        geolocalizacao = geolocator.geocode(local[0] + ', ' + local[1])
        quantidadeNascimento = contNascimento.loc[local]['Quantidade'].item()
        if geolocalizacao is not None:
            elementoNascimento = [geolocalizacao.latitude, geolocalizacao.longitude, quantidadeNascimento]
            coordenadasNascimento.append(elementoNascimento)
    except:
        pass

#locate the work places coordinates and register their occurrences number
for local in contAtuacao.index:
    try:
        print(local)
        geolocalizacao = geolocator.geocode(local[0] + ', ' + local[1])
        quantidadeAtuacao = contAtuacao.loc[local]['Quantidade'].item()
        if geolocalizacao is not None:
            elementoAtuacao = [geolocalizacao.latitude, geolocalizacao.longitude, quantidadeAtuacao]
            coordenadasAtuacao.append(elementoAtuacao)
    except:
        pass

# %%
#generate the maps
mapaNascimento = folium.Map(width='100%',
                    height='100%',
                    location=[-15.77972, -47.92972],
                    zoom_start=4)
HeatMap(coordenadasNascimento, radius=10).add_to(mapaNascimento)

mapaAtuacao = folium.Map(width='100%',
                    height='100%',
                    location=[-15.77972, -47.92972],
                    zoom_start=4)
HeatMap(coordenadasAtuacao, radius=10).add_to(mapaAtuacao)

#save the maps in a html file
mapaNascimento.save('./results/visualization/mapaNascimento.html')
mapaAtuacao.save('./results/visualization/mapaAtuacao.html')
# %%

nosUniversidade = pd.read_csv('./results/primary/conexoesUniversidade.csv', sep=',')

source = nosUniversidade['Origem'].unique() 
target = nosUniversidade['Destino'].unique()

nos = pd.concat([pd.DataFrame(source), pd.DataFrame(target)], axis=0).drop_duplicates().reset_index(drop=True)
nos.to_csv('./results/graph/nos.csv', sep=',', encoding='utf-8', index=False)
