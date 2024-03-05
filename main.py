# %%
#!/usr/bin/python
# -*- coding: utf-8 -*-
import glob
import csv
import io
import zipfile
import string
import pandas as pd

from lxml import etree

# %%
#for testing
inicio = int(input('Informe o início: '))
fim = int(input('Informe o fim: '))
curriculos = glob.glob('db/CurriculosBRA/*/*/*/*/*')
cont = 0

# %%
#creates a list to store the header of the csv files with identifiers and education
HISTORICOS_HEADER = ['ENSINO-MEDIO-SEGUNDO-GRAU', 'Instituição'.encode('utf-8').decode('utf-8'),
                    'Início'.encode('utf-8').decode('utf-8'), 'Fim',
                    'CURSO-TECNICO-PROFISSIONALIZANTE', 'Instituição'.encode('utf-8').decode('utf-8'),
                    'Início'.encode('utf-8').decode('utf-8'), 'Fim', 
                    'GRADUACAO',  'Instituição'.encode('utf-8').decode('utf-8'),
                    'Início'.encode('utf-8').decode('utf-8'), 'Fim', 
                    'ESPECIALIZACAO',  'Instituição'.encode('utf-8').decode('utf-8'),
                    'Início'.encode('utf-8').decode('utf-8'), 'Fim', 
                    'MESTRADO',  'Instituição'.encode('utf-8').decode('utf-8'),
                    'Início'.encode('utf-8').decode('utf-8'), 'Fim', 
                    'DOUTORADO',  'Instituição'.encode('utf-8').decode('utf-8'),
                    'Início'.encode('utf-8').decode('utf-8'), 'Fim']

#the university name
UNIVERSIDADE = 'Centro Federal de Educação Tecnológica de Minas Gerais'
UNIVERSIDADE_SIGLA = 'CEFET-MG'
UNIVERSIDADE_SIGLA2 = 'CEFET/MG'
UNIVERSIDADE_SIGLA3 = 'CEFET - MG'

#the index of the courses that are able to be connected
INDEX_CONEXAO = (4, 8, 16, 20)

# %%
#starts a series to store the total quantity of each course concluded
contHistoricosTotal = pd.Series(index=['CURSO-TECNICO-PROFISSIONALIZANTE',
                                        'GRADUACAO',
                                        'MESTRADO',
                                        'DOUTORADO'], dtype='int64')
contHistoricosTotal.iloc[:] = 0
#starts the csv files with identifiers and education
historicos_file = open('./results/primary/historicos.csv', 'w', encoding='utf-8', newline='')
historicos_handle = csv.writer(historicos_file, delimiter=',')
historicos_handle.writerow(['Identificador']+HISTORICOS_HEADER)

#starts the csv files with identifiers and education in the university
historicoUniversidade_file = open('./results/primary/historicosUniversidade.csv', 'w', encoding='utf-8', newline='')
historicosUniversidade_handle = csv.writer(historicoUniversidade_file, delimiter=',')
historicosUniversidade_handle.writerow(['Identificador']+HISTORICOS_HEADER)

#starts the csv files with identifiers and the university score
pontuacaoIndividual_file = open('./results/primary/pontuacaoIndividual.csv', 'w', encoding='utf-8', newline='')
pontuacaoIndividual_handle = csv.writer(pontuacaoIndividual_file, delimiter=',')
pontuacaoIndividual_handle.writerow(['Identificador', 'Pontuação'])

#starts the csv files with identifiers and birth places
localizacao_file = open('./results/primary/localizacao.csv', 'w', encoding='utf-8', newline='')
localizacao_handle = csv.writer(localizacao_file, delimiter=',')
localizacao_handle.writerow(['Identificador',
                            'Cidade de Origem', 'Estado de Origem',
                            'País de Origem'.encode('utf-8').decode('utf-8'),
                            'Instituição de Atuação'.encode('utf-8').decode('utf-8'),
                            'Cidade de Atuação'.encode('utf-8').decode('utf-8'), 'Estado de Atuação'.encode('utf-8').decode('utf-8'),
                            'País de Atuação'.encode('utf-8').decode('utf-8')])

#starts the csv files with the connections between the univesities
conexoesUniversidade_file = open('./results/primary/conexoesUniversidade.csv', 'w', encoding='utf-8', newline='')
conexoesUniversidade_handle = csv.writer(conexoesUniversidade_file, delimiter=',')
conexoesUniversidade_handle.writerow(['Origem', 'Destino'])

# %%
for curriculo in curriculos:
    #if int(inicio)-1 <= int(cont) < int(fim):
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

        #get the identifier and the education
        identificador = root.xpath('string(/CURRICULO-VITAE/@NUMERO-IDENTIFICADOR)')
        formacoes = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/*')

        #reset the check variable and the series
        universityFound = False
        universityScore = 0

        historico = pd.Series(index=HISTORICOS_HEADER, dtype='object')
        historicoUniversidade = pd.Series(index=HISTORICOS_HEADER, dtype='object')
        conexoesUniversidade = pd.DataFrame(columns=['Origem', 'Destino'], dtype='object')

        historico.iloc[:] = None
        historicoUniversidade.iloc[:] = None

        for formacao in formacoes:
            #get the formatted course name
            nomeCurso = string.capwords(formacao.xpath('string(./@NOME-CURSO)').encode('utf-8').decode('utf-8')).replace('Curso', '').replace('Técnico Em ', '').replace('Tecnico Em ', '').replace('Técnico De ', '').replace('Tecnico De ', '').replace('Técnico', '').replace('Tecnico', '').replace('Graduação Em ', '').replace('Licenciatura Em ', '').replace('Bacharelado Em ', '').replace('Especialização Em ', '').replace('Mestrado Em ', '').replace('Doutorado Em ', '').replace('Curso De ', '')
            #get the index of the current course
            indexFormacao = historico.index.get_loc(formacao.tag)

            #check the university
            #if formacao.xpath('string(./@NOME-INSTITUICAO)') == UNIVERSIDADE:
            if UNIVERSIDADE in formacao.xpath('string(./@NOME-INSTITUICAO)') or UNIVERSIDADE_SIGLA in formacao.xpath('string(./@NOME-INSTITUICAO)') or UNIVERSIDADE_SIGLA2 in formacao.xpath('string(./@NOME-INSTITUICAO)') or UNIVERSIDADE_SIGLA3 in formacao.xpath('string(./@NOME-INSTITUICAO)'):
                #if is the university, set the check variable to true and add one to the score
                universityFound = True
                universityScore += 1

                #add the course to the university dataframe
                historicoUniversidade.iloc[indexFormacao:indexFormacao+4] = nomeCurso, formacao.xpath('string(./@NOME-INSTITUICAO)'), formacao.xpath('string(./@ANO-DE-INICIO)'), formacao.xpath('string(./@ANO-DE-CONCLUSAO)')

                #add the course to the general dataframe
                historico.iloc[indexFormacao:indexFormacao+4] = nomeCurso, formacao.xpath('string(./@NOME-INSTITUICAO)'), formacao.xpath('string(./@ANO-DE-INICIO)'), formacao.xpath('string(./@ANO-DE-CONCLUSAO)')

            #if isn't the university, check if the course is already in the series
            elif pd.isnull(historico.iloc[indexFormacao]):
                historico.iloc[indexFormacao:indexFormacao+4] = nomeCurso, formacao.xpath('string(./@NOME-INSTITUICAO)'), formacao.xpath('string(./@ANO-DE-INICIO)'), formacao.xpath('string(./@ANO-DE-CONCLUSAO)')

            #if the course exists, add one to the total of courses
            if historico.iloc[indexFormacao+3]:
                contHistoricosTotal[formacao.tag] += 1

            #check if the course is able to be connected
            if indexFormacao in INDEX_CONEXAO and indexFormacao != 4:
                #if is able, get the index of the previous course
                iFormacaoAnterior = INDEX_CONEXAO[INDEX_CONEXAO.index(indexFormacao)-1]
                #add the connection to the dataframe
                conexoesUniversidade = pd.concat([conexoesUniversidade, pd.DataFrame([[str(historico.iloc[iFormacaoAnterior+1])+'/'+str(historico.index[iFormacaoAnterior])+'/'+str(historico.iloc[iFormacaoAnterior]), historico.iloc[indexFormacao+1]+'/'+str(historico.index[indexFormacao])+'/'+historico.iloc[indexFormacao]]], columns=['Origem', 'Destino'])], ignore_index=True)

        #add the total of courses to the series
        pd.DataFrame(contHistoricosTotal).T.to_csv('./results/quantitative/contHistoricosTotal.csv', sep=',', encoding='utf-8', index=False, mode='w')
        
        #check if the university was found
        if universityFound:
            #if was found, add the data with the identifier to the files
            historico = historico.to_list()
            historico[0:0] = [identificador]
            historicos_handle.writerow(historico)

            historicoUniversidade = historicoUniversidade.to_list()
            historicoUniversidade[0:0] = [identificador]
            historicosUniversidade_handle.writerow(historicoUniversidade)

            pontuacaoIndividual_handle.writerow([identificador, universityScore])

            localNacimento = [root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@CIDADE-NASCIMENTO)'),
                            root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@UF-NASCIMENTO)'),
                            root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@PAIS-DE-NASCIMENTO)')]

            #check if the person is working
            if not root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/ENDERECO/ENDERECO-PROFISSIONAL/@NOME-INSTITUICAO-EMPRESA)'):
                #if isn't working, check if the person is studying
                if not root.xpath('string((/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS//VINCULOS[@ANO-FIM=""]/../@NOME-INSTITUICAO)[1])'):
                    #if isn't studying, add the earliest university to the file
                    localizacao_handle.writerow([identificador] +
                                                localNacimento +
                                                [root.xpath('string((/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS//VINCULOS[not(/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS//VINCULOS/@ANO-FIM > @ANO-FIM)]/../@NOME-INSTITUICAO)[1])')])
                else:
                    #if is studying, add the university to the file
                    localizacao_handle.writerow([identificador] +
                                                localNacimento +
                                                [root.xpath('string((/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS//VINCULOS[@ANO-FIM=""]/../@NOME-INSTITUICAO)[1])')])
            else:
                #if is working, add the work place to the file
                localizacao_handle.writerow([identificador] +
                                            localNacimento +
                                            [root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/ENDERECO/ENDERECO-PROFISSIONAL/@NOME-INSTITUICAO-EMPRESA)'),
                                            root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/ENDERECO/ENDERECO-PROFISSIONAL/@CIDADE)'),
                                            root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/ENDERECO/ENDERECO-PROFISSIONAL/@UF)'),
                                            root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/ENDERECO/ENDERECO-PROFISSIONAL/@PAIS)')])

            #add the connections to the file
            conexoesUniversidade = conexoesUniversidade[conexoesUniversidade['Origem'].astype(bool)]
            conexoesUniversidade = conexoesUniversidade.values.tolist()
            conexoesUniversidade_handle.writerows(conexoesUniversidade)

    except Exception as e:
        print(e)

    print(cont)
    cont += 1

#close the files
localizacao_file.close()
historicos_file.close()
historicoUniversidade_file.close()
pontuacaoIndividual_file.close()
conexoesUniversidade_file.close()
# %%
