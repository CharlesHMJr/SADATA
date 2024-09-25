#!/usr/bin/python
# -*- coding: utf-8 -*-
import glob
import csv
import io
import zipfile
import string
import pandas as pd

from lxml import etree

def general_mining():
    CURRICULOS = glob.glob('db/pqs/*/*/*/*')
    OUTPUT = 'pq'

    #creates a list to store the header of the csv files with identifiers and education ####################
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

    #the index of the courses that are able to be connected ####################
    IDXS_PARA_CONEXAO = (4, 8, 16, 20)

    #starts a series to store the total quantity of each course concluded ####################
    qte_total_de_formacoes = pd.Series(index=['CURSO-TECNICO-PROFISSIONALIZANTE',
                                            'GRADUACAO',
                                            'MESTRADO',
                                            'DOUTORADO'], dtype='int64')
    qte_total_de_formacoes[:] = 0

    #starts the csv files with identifiers and education ####################
    historicos_file = open(f'./results/{OUTPUT}/general/primary/historicos.csv', 'w', encoding='utf-8', newline='')
    historicos_handle = csv.writer(historicos_file, delimiter=',')
    historicos_handle.writerow(['Identificador']+HISTORICOS_HEADER)

    #starts the csv files with identifiers, ######################
    #birth places and the institution of work ####################
    localizacao_file = open(f'./results/{OUTPUT}/general/primary/localizacao.csv', 'w', encoding='utf-8', newline='')
    localizacao_handle = csv.writer(localizacao_file, delimiter=',')
    localizacao_handle.writerow(['Identificador',
                                'Cidade de Origem', 'Estado de Origem',
                                'País de Origem'.encode('utf-8').decode('utf-8'),
                                'Instituição de Atuação'.encode('utf-8').decode('utf-8'),
                                'Cidade de Atuação'.encode('utf-8').decode('utf-8'), 'Estado de Atuação'.encode('utf-8').decode('utf-8'),
                                'País de Atuação'.encode('utf-8').decode('utf-8')])

    #starts the csv files with the connections between the univesities ####################
    conexoes_entre_universidades_file = open(f'./results/{OUTPUT}/general/primary/conexoes_entre_universidades.csv', 'w', encoding='utf-8', newline='')
    conexoes_entre_universidades_handle = csv.writer(conexoes_entre_universidades_file, delimiter=',')
    conexoes_entre_universidades_handle.writerow(['Origem', 'Destino'])

    #starts the csv files with the fields of research ####################
    areas_de_atuacao_file = open(f'./results/{OUTPUT}/general/primary/areasDeAtuacao.csv', 'w', encoding='utf-8', newline='')
    areas_de_atuacao_handle = csv.writer(areas_de_atuacao_file, delimiter=',')
    areas_de_atuacao_handle.writerow(['Identificador', 'Grande Área','Área'])

    #iterate over the curriculums ####################
    cont = 0
    for curriculo in CURRICULOS:
        try:
            #read the zip file ####################
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

            #create a tree from the xml ####################
            root = etree.XML(content)

            #get the person's information ####################
            identificador = root.xpath('string(/CURRICULO-VITAE/@NUMERO-IDENTIFICADOR)')
            grande_area_de_atuacao = root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/AREAS-DE-ATUACAO/AREA-DE-ATUACAO[1]/@NOME-GRANDE-AREA-DO-CONHECIMENTO)')
            area_de_atuacao = root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/AREAS-DE-ATUACAO/AREA-DE-ATUACAO[1]/@NOME-DA-AREA-DO-CONHECIMENTO)')
            formacoes = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/*')
            local_de_nascimento = [root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@CIDADE-NASCIMENTO)'),
                    root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@UF-NASCIMENTO)'),
                    root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@PAIS-DE-NASCIMENTO)')]

            #create a series to store the historical of #############################
            #the person and a dataframe to store the connections ####################
            #between the universities ###############################################
            historico = pd.Series(index=HISTORICOS_HEADER, dtype='object')
            conexoes_entre_universidades = pd.DataFrame(columns=['Origem', 'Destino'], dtype='object')

            #iterate over the courses ####################
            for formacao in formacoes:
                #get the formatted course name, ##########################
                #institution name, start and end year ####################
                nome_do_curso = string.capwords(formacao.xpath('string(./@NOME-CURSO)').encode('utf-8').decode('utf-8')).replace('Curso', '').replace('Técnico Em ', '').replace('Tecnico Em ', '').replace('Técnico De ', '').replace('Tecnico De ', '').replace('Técnico', '').replace('Tecnico', '').replace('Graduação Em ', '').replace('Licenciatura Em ', '').replace('Bacharelado Em ', '').replace('Especialização Em ', '').replace('Mestrado Em ', '').replace('Doutorado Em ', '').replace('Curso De ', '')
                nome_da_instituição = string.capwords(formacao.xpath('string(./@NOME-INSTITUICAO)').encode('utf-8').decode('utf-8'))
                inicio_do_curso = formacao.xpath('string(./@ANO-DE-INICIO)')
                fim_do_curso = formacao.xpath('string(./@ANO-DE-CONCLUSAO)')

                #get the index of the current course ####################
                idx_formacao_atual = historico.index.get_loc(formacao.tag)

                #check if the current course is already in the series ####################
                if pd.isnull(historico.iloc[idx_formacao_atual]):
                    #if not, add the course to the series ####################
                    historico.iloc[idx_formacao_atual:idx_formacao_atual+4] = nome_do_curso, nome_da_instituição, inicio_do_curso, fim_do_curso

                #check if the course is concluded ####################
                if historico.iloc[idx_formacao_atual+3]:
                    #if is concluded, add to the total ####################
                    #quantity of courses concluded ########################
                    qte_total_de_formacoes[formacao.tag] += 1

                #check if the course is able to be connected ####################
                if idx_formacao_atual in IDXS_PARA_CONEXAO and idx_formacao_atual != 4:
                    #if is able, get the index of the previous course ####################
                    idx_formacao_anterior = IDXS_PARA_CONEXAO[IDXS_PARA_CONEXAO.index(idx_formacao_atual)-1]
                    #add the connection to the dataframe ####################
                    conexoes_entre_universidades = pd.concat([conexoes_entre_universidades, pd.DataFrame([[str(historico.iloc[idx_formacao_anterior+1])+'/'+str(historico.index[idx_formacao_anterior])+'/'+str(historico.iloc[idx_formacao_anterior]), historico.iloc[idx_formacao_atual+1]+'/'+str(historico.index[idx_formacao_atual])+'/'+historico.iloc[idx_formacao_atual]]], columns=['Origem', 'Destino'])], ignore_index=True)

            #check if the person is working ####################
            if root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/ENDERECO/ENDERECO-PROFISSIONAL/@NOME-INSTITUICAO-EMPRESA)'):
                #if is working, get the institution ####################
                #name, city, state and country #########################
                localizacao = [identificador] + local_de_nascimento + [root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/ENDERECO/ENDERECO-PROFISSIONAL/@NOME-INSTITUICAO-EMPRESA)'),
                    root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/ENDERECO/ENDERECO-PROFISSIONAL/@CIDADE)'),
                    root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/ENDERECO/ENDERECO-PROFISSIONAL/@UF)'),
                    root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/ENDERECO/ENDERECO-PROFISSIONAL/@PAIS)')]
            #if is not working, check if the person is studying ####################
            elif root.xpath('string((/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS//VINCULOS[@ANO-FIM=""]/../@NOME-INSTITUICAO)[1])'):
                #if is studying, get the institution name ####################
                localizacao = [identificador] + local_de_nascimento + [root.xpath('string((/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS//VINCULOS[@ANO-FIM=""]/../@NOME-INSTITUICAO)[1])')]
            else:
                #if is not working or studying, ####################
                #get the last institution name #####################
                localizacao = [identificador] + local_de_nascimento + [root.xpath('string((/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS//VINCULOS[not(/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS//VINCULOS/@ANO-FIM > @ANO-FIM)]/../@NOME-INSTITUICAO)[1])')]

            #add the fields of research to the file
            areas_de_atuacao_handle.writerow([identificador, grande_area_de_atuacao, area_de_atuacao])

            #add the historical to the file
            historico = historico.to_list()
            historico[0:0] = [identificador]
            historicos_handle.writerow(historico)

            #add the connections to the file
            conexoes_entre_universidades = conexoes_entre_universidades[conexoes_entre_universidades['Origem'].astype(bool)]
            conexoes_entre_universidades = conexoes_entre_universidades.values.tolist()
            conexoes_entre_universidades_handle.writerows(conexoes_entre_universidades)

            #add the birth place and the current institution to the file
            localizacao_handle.writerow(localizacao)

        except (FileNotFoundError, zipfile.BadZipFile, etree.XMLSyntaxError, KeyError) as e:
            print(f"Error: {e}")

        print(cont)
        cont += 1

    #add the total of courses to the file
    pd.DataFrame(qte_total_de_formacoes).T.to_csv(f'./results/{OUTPUT}/general/quantitative/contFormacoesTotal.csv', sep=',', encoding='utf-8', index=False, mode='w')

    #close the files
    localizacao_file.close()
    historicos_file.close()
    conexoes_entre_universidades_file.close()
    areas_de_atuacao_file.close()