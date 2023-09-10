# %%
#!/usr/bin/python
# -*- coding: utf-8 -*-
import glob
import csv
import io
import zipfile
import folium

import pandas as pd

from geopy.geocoders import Nominatim
from lxml import etree
from folium.plugins import HeatMap

# %%
#for testing
inicio = int(input('Informe o início: '))
fim = int(input('Informe o fim: '))
curriculos = glob.glob('collection/*/*')
cont = 0

#creates a list to store the header of the csv files with identifiers and education
historicosHeader = ['Identificador', 
                        'ENSINO-MEDIO-SEGUNDO-GRAU', 'Instituição'.encode('utf-8').decode('utf-8'),'Início'.encode('utf-8').decode('utf-8'), 'Fim',
                        'CURSO-TECNICO-PROFISSIONALIZANTE',  'Instituição'.encode('utf-8').decode('utf-8'),'Início'.encode('utf-8').decode('utf-8'), 'Fim', 
                        'GRADUACAO',  'Instituição'.encode('utf-8').decode('utf-8'),'Início'.encode('utf-8').decode('utf-8'), 'Fim', 
                        'ESPECIALIZACAO',  'Instituição'.encode('utf-8').decode('utf-8'),'Início'.encode('utf-8').decode('utf-8'), 'Fim', 
                        'MESTRADO',  'Instituição'.encode('utf-8').decode('utf-8'),'Início'.encode('utf-8').decode('utf-8'), 'Fim', 
                        'DOUTORADO',  'Instituição'.encode('utf-8').decode('utf-8'),'Início'.encode('utf-8').decode('utf-8'), 'Fim']

#starts the csv files with identifiers and education
historicos_file = open('historicos.csv', 'w', encoding='utf-8', newline='')
historicos_handle = csv.writer(historicos_file, delimiter='\t')
historicos_handle.writerow(historicosHeader)

#starts the csv files with identifiers and education in the university
historicoUniversidade_file = open('historicosUniversidade.csv', 'w', encoding='utf-8', newline='')
historicosUniversidade_handle = csv.writer(historicoUniversidade_file, delimiter='\t')
historicosUniversidade_handle.writerow(historicosHeader)

#starts the csv files with identifiers and birth places
localNascimento_file = open('localNascimento.csv', 'w', encoding='utf-8', newline='')
localNascimento_handle = csv.writer(localNascimento_file, delimiter='\t')
localNascimento_handle.writerow(['Identificador', 'Cidade', 'Estado', 'País'.encode('utf-8').decode('utf-8')])

#creates a list to store the birth places coordinates
coordenadasNascimento = []

geolocator = Nominatim(user_agent="103962022")
# %%
for curriculo in curriculos:
    if int(inicio)-1 <= int(cont) < int(fim):
        try:
            #read the zip file
            arquivo_handle = open(curriculo, 'rb')
            content = arquivo_handle.read()
            if curriculo.split('.')[-1] == 'zip':
                if type(content) is type(str):
                    content = content
                zip_memory = io.BytesIO(content)
                zip_data = zipfile.ZipFile(zip_memory)
                xml = b''
                for fn in zip_data.namelist():
                    xml += zip_data.read(fn)
                content = xml

            #create a tree from the xml
            root = etree.XML(content)

            #get the identifier and the education
            identificador = root.xpath('string(/CURRICULO-VITAE/@NUMERO-IDENTIFICADOR)')
            formacoes = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/*')

            #reset the check variable and the series
            universityFound = False
            historico = pd.Series(index=historicosHeader, dtype='object')
            historicoUniversidade = pd.Series(index=historicosHeader, dtype='object')
            historico.iloc[:] = None
            historicoUniversidade.iloc[:] = None

            for formacao in formacoes:
                #get the index of the current course
                indexFormacao = historico.index.get_loc(formacao.tag)
                #check the university
                if formacao.xpath('string(./@NOME-INSTITUICAO)') == 'Centro Federal de Educação Tecnológica de Minas Gerais':
                    universityFound = True
                    #add the course to the university dataframe
                    historicoUniversidade.iloc[indexFormacao:indexFormacao+4] = formacao.xpath('string(./@NOME-CURSO)'), formacao.xpath('string(./@NOME-INSTITUICAO)'), formacao.xpath('string(./@ANO-DE-INICIO)'), formacao.xpath('string(./@ANO-DE-CONCLUSAO)')
                    #add the course to the general dataframe
                    historico.iloc[indexFormacao:indexFormacao+4] = formacao.xpath('string(./@NOME-CURSO)'), formacao.xpath('string(./@NOME-INSTITUICAO)'), formacao.xpath('string(./@ANO-DE-INICIO)'), formacao.xpath('string(./@ANO-DE-CONCLUSAO)')
                #if isn't the university, check if the course is already in the series
                elif pd.isnull(historico.iloc[indexFormacao]):
                    historico.iloc[indexFormacao:indexFormacao+4] = formacao.xpath('string(./@NOME-CURSO)'), formacao.xpath('string(./@NOME-INSTITUICAO)'), formacao.xpath('string(./@ANO-DE-INICIO)'), formacao.xpath('string(./@ANO-DE-CONCLUSAO)')

            #if the university was found, add the series to the file
            if universityFound:
                historico = historico.to_list()
                historico[0:0] = [identificador]
                historicos_handle.writerow(historico)

                historicoUniversidade = historicoUniversidade.to_list()
                historicoUniversidade[0:0] = [identificador]
                historicosUniversidade_handle.writerow(historicoUniversidade)

                localNascimento_handle.writerow([identificador, root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@CIDADE-NASCIMENTO)'), root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@UF-NASCIMENTO)'), root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@PAIS-DE-NASCIMENTO)')])

        except:
            pass

    cont += 1

#close the files
localNascimento_file.close()
historicos_file.close()
historicoUniversidade_file.close()

# %%
#count the birth places
contagemNascimento = pd.read_csv('localNascimento.csv', sep='\t')
contagemNascimento = contagemNascimento.value_counts(['Cidade', 'Estado']).to_frame('Quantidade')
contagemNascimento.to_csv('contagemNascimento.csv', sep='\t', encoding='utf-8')

# %%
#locate the birth places coordinates and register their occurrences number
for local in contagemNascimento.index:
    try:
        geolocalNascimento = geolocator.geocode(local[0] + ', ' + local[1])
        quantidadeNascimento = contagemNascimento.loc[local]['Quantidade'].item()
        if geolocalNascimento is not None:
            elementoNascimento = [geolocalNascimento.latitude, geolocalNascimento.longitude, quantidadeNascimento]
            coordenadasNascimento.append(elementoNascimento)
    except:
        pass

# %%
#generate the map
baseMap = folium.Map(width='100%', 
                    height='100%', 
                    location=[-15.77972, -47.92972], 
                    zoom_start=4)
HeatMap(coordenadasNascimento, radius=12).add_to(baseMap)

#save the map in a html file
baseMap.save('mapa.html')
