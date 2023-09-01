# %%

#!/usr/bin/python
# -*- coding: utf-8 -*-

import io
import zipfile

import glob
import pandas as pd
from lxml import etree
from geopy.geocoders import Nominatim
import folium
from folium.plugins import HeatMap
# %%
#for testing
inicio = int(input('Informe o início: '))
fim = int(input('Informe o fim: '))
curriculos = glob.glob('collection/*/*')
cont = 0

#creates a dataframe to store indentifiers and birth places
localNascimento = pd.DataFrame(columns=['Identificador', 'Cidade', 'Estado', 'País'], dtype='object', index=['Identificador'])

coordenadasNascimento = []

#creates a dataframe to store indentifiers and education
historicos = pd.DataFrame(columns=['Identificador', 
                                   'ENSINO-MEDIO-SEGUNDO-GRAU', 'Instituição','Início', 'Fim',
                                   'CURSO-TECNICO-PROFISSIONALIZANTE',  'Instituição','Início', 'Fim', 
                                   'GRADUACAO',  'Instituição','Início', 'Fim', 
                                   'ESPECIALIZACAO',  'Instituição','Início', 'Fim', 
                                   'MESTRADO',  'Instituição','Início', 'Fim', 
                                   'DOUTORADO',  'Instituição','Início', 'Fim'],dtype='object', index=['Identificador'])
# creates a series to store the current identifier and education
historico = pd.Series(index=historicos.columns, dtype='object')

# creates a dataframe to store indentifiers and education in the university
historicosUniversidade = pd.DataFrame(columns=historicos.columns, dtype='object', index=['Identificador'])

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
                    content = content.encode('utf-8')
                zip_memory = io.BytesIO(content)
                zip_data = zipfile.ZipFile(zip_memory)
                xml = b''
                for fn in zip_data.namelist():
                    xml += zip_data.read(fn)
                content = xml

            #create a tree from the xml
            root = etree.XML(content)
            identificador = root.xpath('string(/CURRICULO-VITAE/@NUMERO-IDENTIFICADOR)')
            formacoes = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/*')

            #reset the check variable and the series
            universityFound = False
            historico.iloc[:] = None
            #define the identifier in the series
            historico['Identificador'] = identificador
            for formacao in formacoes:
                #get the index of the current course
                indexFormacao = historico.index.get_loc(formacao.tag)
                #check the university
                if formacao.xpath('string(./@NOME-INSTITUICAO)') == 'Centro Federal de Educação Tecnológica de Minas Gerais':
                    universityFound = True
                    #add the course to the university dataframe
                    historicosUniversidade.loc[identificador, 'Identificador'] = identificador
                    historicosUniversidade.iloc[historicosUniversidade.index.get_loc(identificador), indexFormacao:indexFormacao+4] = formacao.xpath('string(./@NOME-CURSO)'), formacao.xpath('string(./@NOME-INSTITUICAO)'), formacao.xpath('string(./@ANO-DE-INICIO)'), formacao.xpath('string(./@ANO-DE-CONCLUSAO)')
                    #add the course to the general dataframe
                    historico.iloc[indexFormacao:indexFormacao+4] = formacao.xpath('string(./@NOME-CURSO)'), formacao.xpath('string(./@NOME-INSTITUICAO)'), formacao.xpath('string(./@ANO-DE-INICIO)'), formacao.xpath('string(./@ANO-DE-CONCLUSAO)')
                #if isn't the university, check if the course is already in the series
                elif pd.isnull(historico.iloc[indexFormacao]):
                    historico.iloc[indexFormacao:indexFormacao+4] = formacao.xpath('string(./@NOME-CURSO)'), formacao.xpath('string(./@NOME-INSTITUICAO)'), formacao.xpath('string(./@ANO-DE-INICIO)'), formacao.xpath('string(./@ANO-DE-CONCLUSAO)')

            #if the university was found, add the series to the dataframe
            if universityFound:
                historicos.loc[identificador] = historico
                localNascimento.loc[identificador] = identificador, root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@CIDADE-NASCIMENTO)'), root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@UF-NASCIMENTO)'), root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@PAIS-DE-NASCIMENTO)')

        except:
            pass
    cont += 1
# %%
historicos.drop(index='Identificador', inplace=True)
historicos.to_csv('historicos.csv', sep='\t', encoding='utf-8', index=False)

historicosUniversidade.drop(index='Identificador', inplace=True)
historicosUniversidade.to_csv('historicosUniversidade.csv', sep='\t', encoding='utf-8', index=False)

localNascimento.drop(index='Identificador', inplace=True)
localNascimento.to_csv('localNascimento.csv', sep='\t', encoding='utf-8', index=False)

contagemNascimento = localNascimento.value_counts(['Cidade', 'Estado']).to_frame('Quantidade')
contagemNascimento.to_csv('contagemNascimento.csv', sep='\t', encoding='utf-8')
# %%
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
baseMap = folium.Map(width='100%', 
                    height='100%', 
                    location=[-15.77972, -47.92972], 
                    zoom_start=4)
HeatMap(coordenadasNascimento, radius=12).add_to(baseMap)
