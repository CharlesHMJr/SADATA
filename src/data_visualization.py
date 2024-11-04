#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import folium

from folium.plugins import HeatMap
from geopy.geocoders import Nominatim

def data_visualization():
    OUTPUT = 'new'
    ANALISE_ESPECIFICA = False

    if ANALISE_ESPECIFICA:
        DIR = f'./results/{OUTPUT}/specific'
    else:
        DIR = f'./results/{OUTPUT}/general'

    #creates a geolocator to locate the birth places and current institutions ####################
    geolocator = Nominatim(user_agent="103962022")

    #creates a list to store the birth places #######################
    #coordinates and the current institutions coordinates ####################
    coordenadas_local_de_nascimento = []
    coordenadas_local_de_atuacao = []

    qte_local_de_nascimento = pd.read_csv(f'{DIR}/quantitative/cont_localizacao_de_nascimento.csv', sep=',')
    qte_local_de_nascimento.set_index(['Cidade de Origem', 'Estado de Origem'], inplace=True)
    qte_local_de_atuacao = pd.read_csv(f'{DIR}/quantitative/cont_localizacao_de_atuacao.csv', sep=',')
    qte_local_de_atuacao.set_index(['Cidade de Atuação', 'Estado de Atuação'], inplace=True)

    #iterate over the birth places ####################
    for local in qte_local_de_nascimento.index:
        try:
            #locate the birth places coordinates ####################
            geolocalizacao = geolocator.geocode(local[0] + ', ' + local[1], timeout=None)
            #register the occurrences number ####################
            qte_local_de_nascimento_atual = qte_local_de_nascimento.loc[local]['Quantidade'].item()
            #check if the birth place has coordinates ####################
            if geolocalizacao is not None:
                #if it has, create a list with the #########################
                #coordinates and the occurrences number ####################
                coordenadas_local_de_nascimento_atual = [geolocalizacao.latitude, geolocalizacao.longitude, qte_local_de_nascimento_atual]
                print(coordenadas_local_de_nascimento_atual)
                #add the list to the birth places list ####################
                coordenadas_local_de_nascimento.append(coordenadas_local_de_nascimento_atual)
        except Exception as e:
            print(e)

    #iterate over the current institutions ####################
    for local in qte_local_de_atuacao.index:
        try:
            #locate the current institutions coordinates ####################
            geolocalizacao = geolocator.geocode(local[0] + ', ' + local[1], timeout=None)
            #register the occurrences number ####################
            qte_local_de_atuacao_atual = qte_local_de_atuacao.loc[local]['Quantidade'].item()
            #check if the current institution has coordinates ####################
            if geolocalizacao is not None:
                #if it has, create a list with the #########################
                #coordinates and the occurrences number ####################
                coordenadas_local_de_atuacao_atual = [geolocalizacao.latitude, geolocalizacao.longitude, qte_local_de_atuacao_atual]
                print(coordenadas_local_de_atuacao_atual)
                #add the list to the current institutions list ####################
                coordenadas_local_de_atuacao.append(coordenadas_local_de_atuacao_atual)
        except Exception as e:
            print(e)

    #generate the maps
    mapaNascimento = folium.Map(width='100%',
                        height='100%',
                        location=[-15.77972, -47.92972],
                        zoom_start=4)
    HeatMap(coordenadas_local_de_nascimento, radius=10).add_to(mapaNascimento)

    mapaAtuacao = folium.Map(width='100%',
                        height='100%',
                        location=[-15.77972, -47.92972],
                        zoom_start=4)
    HeatMap(coordenadas_local_de_atuacao, radius=10).add_to(mapaAtuacao)

    #save the maps in a html file
    mapaNascimento.save(f'{DIR}/visualization/mapa_de_calor_por_nascimento.html')
    mapaAtuacao.save(f'{DIR}/visualization/mapa_de_calor_por_atuacao.html')

    #get the connections (edges) between the universities ####################
    arestas_entre_universidades = pd.read_csv(f'{DIR}/primary/conexoes_entre_universidades.csv', sep=',')

    #get the universities (nodes) from the connections ####################
    nos_de_origem = arestas_entre_universidades['Origem'].unique()
    nos_de_destino = arestas_entre_universidades['Destino'].unique()
    #create a csv file with the universities ####################
    nos = pd.concat([pd.DataFrame(nos_de_origem), pd.DataFrame(nos_de_destino)], axis=0).drop_duplicates().reset_index(drop=True)
    nos.to_csv(f'{DIR}/graph/nos.csv', sep=',', encoding='utf-8', index=False)