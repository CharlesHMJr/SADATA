#!/usr/bin/python
# -*- coding: utf-8 -*-
import glob
import csv
import io
import zipfile
import string
import pandas as pd

from lxml import etree

def specific_mining():
    INICIO = int(input('Informe o início: '))
    FIM = int(input('Informe o fim: '))

    CURRICULOS = glob.glob('db/pqs/*/*/*/*')
    OUTPUT = 'new'

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

    #defines the university to be searched ####################
    UNIVERSIDADE_PROCURADA = 'Centro Federal de Educação Tecnológica de Minas Gerais'
    SIGLA_UNIVERSIDADE_PROCURADA = 'CEFET-MG'
    SIGLA2_UNIVERSIDADE_PROCURADA = 'CEFET/MG'
    SIGLA3_UNIVERSIDADE_PROCURADA = 'CEFET - MG'

    #the index of the courses that are able to be connected ####################
    IDXS_PARA_CONEXAO = (4, 8, 16, 20)

    #starts a series to store the total quantity of each course concluded ####################
    qte_total_de_formacoes = pd.Series(index=['ENSINO-MEDIO-SEGUNDO-GRAU',
                                            'CURSO-TECNICO-PROFISSIONALIZANTE',
                                            'GRADUACAO',
                                            'ESPECIALIZACAO',
                                            'MESTRADO',
                                            'DOUTORADO'], dtype='int64')
    qte_total_de_formacoes[:] = 0

    #starts the csv files with identifiers and education ####################
    historicos_file = open(f'./results/{OUTPUT}/specific/primary/historicos.csv', 'w', encoding='utf-8', newline='')
    historicos_handle = csv.writer(historicos_file, delimiter=',')
    historicos_handle.writerow(['Identificador']+HISTORICOS_HEADER)

    #starts the csv files with identifiers and education in the university ####################
    historico_na_universidade_file = open(f'./results/{OUTPUT}/specific/primary/historicos_na_universidade.csv', 'w', encoding='utf-8', newline='')
    historico_na_universidade_handle = csv.writer(historico_na_universidade_file, delimiter=',')
    historico_na_universidade_handle.writerow(['Identificador']+HISTORICOS_HEADER)

    #starts the csv files with identifiers and the university score ####################
    qte_de_formacoes_na_universidade_file = open(f'./results/{OUTPUT}/specific/primary/pontuacao_individual.csv', 'w', encoding='utf-8', newline='')
    qte_de_formacoes_na_universidade_handle = csv.writer(qte_de_formacoes_na_universidade_file, delimiter=',')
    qte_de_formacoes_na_universidade_handle.writerow(['Identificador', 'Pontuação'])

    #starts the csv files with identifiers, ######################
    #birth places and the institution of work ####################
    localizacao_file = open(f'./results/{OUTPUT}/specific/primary/localizacao.csv', 'w', encoding='utf-8', newline='')
    localizacao_handle = csv.writer(localizacao_file, delimiter=',')
    localizacao_handle.writerow(['Identificador',
                                'Cidade de Origem', 'Estado de Origem',
                                'País de Origem'.encode('utf-8').decode('utf-8'),
                                'Instituição de Atuação'.encode('utf-8').decode('utf-8'),
                                'Cidade de Atuação'.encode('utf-8').decode('utf-8'), 'Estado de Atuação'.encode('utf-8').decode('utf-8'),
                                'País de Atuação'.encode('utf-8').decode('utf-8')])

    #starts the csv files with the connections between the univesities ####################
    conexoes_entre_universidades_file = open(f'./results/{OUTPUT}/specific/primary/conexoes_entre_universidades.csv', 'w', encoding='utf-8', newline='')
    conexoes_entre_universidades_handle = csv.writer(conexoes_entre_universidades_file, delimiter=',')
    conexoes_entre_universidades_handle.writerow(['Origem', 'Destino'])

    #starts the csv files with the fields of research ####################
    areas_de_atuacao_file = open(f'./results/{OUTPUT}/specific/primary/areas_de_atuacao.csv', 'w', encoding='utf-8', newline='')
    areas_de_atuacao_handle = csv.writer(areas_de_atuacao_file, delimiter=',')
    areas_de_atuacao_handle.writerow(['Identificador', 'Grande Área','Área'])

    #iterates over the curriculums ####################
    cont = 0
    for curriculo in CURRICULOS:
        if INICIO <= cont <= FIM:
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

                #get the identifier and the education ####################
                identificador = root.xpath('string(/CURRICULO-VITAE/@NUMERO-IDENTIFICADOR)')
                formacoes = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/*')

                #reset the check variable and the series to #########################
                #store the quantity of courses in the university ####################
                universidade_encontrada = False
                qte_de_formacoes_na_universidade = 0

                #create the series to store the historical of ######################################
                #the person, the historical in the university, the connections #####################
                #between the universities and the quantity of courses concluded ####################
                historico = pd.Series(index=HISTORICOS_HEADER, dtype='object')
                historico_na_universidade = pd.Series(index=HISTORICOS_HEADER, dtype='object')
                conexoes_entre_universidades = pd.DataFrame(columns=['Origem', 'Destino'], dtype='object')
                qte_parcial_de_formacoes = pd.Series(index=['ENSINO-MEDIO-SEGUNDO-GRAU',
                                                'CURSO-TECNICO-PROFISSIONALIZANTE',
                                                'GRADUACAO',
                                                'ESPECIALIZACAO',
                                                'MESTRADO',
                                                'DOUTORADO'], dtype='int64')
                qte_parcial_de_formacoes[:] = 0

                #iterates over the courses ####################
                for formacao in formacoes:
                    if formacao.tag in HISTORICOS_HEADER:
                        #get the index of the current course ####################
                        idx_formacao_atual = historico.index.get_loc(formacao.tag)

                        #check the university ####################
                        if UNIVERSIDADE_PROCURADA in formacao.xpath('string(./@NOME-INSTITUICAO)') or SIGLA_UNIVERSIDADE_PROCURADA in formacao.xpath('string(./@NOME-INSTITUICAO)') or SIGLA2_UNIVERSIDADE_PROCURADA in formacao.xpath('string(./@NOME-INSTITUICAO)') or SIGLA3_UNIVERSIDADE_PROCURADA in formacao.xpath('string(./@NOME-INSTITUICAO)'):
                            #if is the university, set the check ##########################
                            #variable to true and add one to the score ####################
                            universidade_encontrada = True
                            qte_de_formacoes_na_universidade += 1

                            #get the course data ####################
                            nome_do_curso = string.capwords(formacao.xpath('string(./@NOME-CURSO)').encode('utf-8').decode('utf-8')).replace('Curso', '').replace('Técnico Em ', '').replace('Tecnico Em ', '').replace('Técnico De ', '').replace('Tecnico De ', '').replace('Técnico', '').replace('Tecnico', '').replace('Graduação Em ', '').replace('Licenciatura Em ', '').replace('Bacharelado Em ', '').replace('Especialização Em ', '').replace('Mestrado Em ', '').replace('Doutorado Em ', '').replace('Curso De ', '')
                            nome_da_instituição = string.capwords(formacao.xpath('string(./@NOME-INSTITUICAO)').encode('utf-8').decode('utf-8'))
                            inicio_do_curso = formacao.xpath('string(./@ANO-DE-INICIO)')
                            fim_do_curso = formacao.xpath('string(./@ANO-DE-CONCLUSAO)')

                            #add the course to the university dataframe ####################
                            historico_na_universidade.iloc[idx_formacao_atual:idx_formacao_atual+4] = nome_do_curso, nome_da_instituição, inicio_do_curso, fim_do_curso

                            #add the course to the general dataframe ####################
                            historico.iloc[idx_formacao_atual:idx_formacao_atual+4] = nome_do_curso, nome_da_instituição, inicio_do_curso, fim_do_curso

                        #if isn't the university, check if the ####################
                        #course is already in the series ##########################
                        elif pd.isnull(historico.iloc[idx_formacao_atual]):
                            #if isn't, get the course data ####################
                            nome_do_curso = string.capwords(formacao.xpath('string(./@NOME-CURSO)').encode('utf-8').decode('utf-8')).replace('Curso', '').replace('Técnico Em ', '').replace('Tecnico Em ', '').replace('Técnico De ', '').replace('Tecnico De ', '').replace('Técnico', '').replace('Tecnico', '').replace('Graduação Em ', '').replace('Licenciatura Em ', '').replace('Bacharelado Em ', '').replace('Especialização Em ', '').replace('Mestrado Em ', '').replace('Doutorado Em ', '').replace('Curso De ', '')
                            nome_da_instituição = string.capwords(formacao.xpath('string(./@NOME-INSTITUICAO)').encode('utf-8').decode('utf-8'))
                            inicio_do_curso = formacao.xpath('string(./@ANO-DE-INICIO)')
                            fim_do_curso = formacao.xpath('string(./@ANO-DE-CONCLUSAO)')

                            #add the course to the general dataframe ####################
                            historico.iloc[idx_formacao_atual:idx_formacao_atual+4] = nome_do_curso, nome_da_instituição, inicio_do_curso, fim_do_curso

                        #check if the course is concluded ####################
                        if historico.iloc[idx_formacao_atual+3]:
                            #if is concluded, add to the total ####################
                            #quantity of courses concluded ########################
                            qte_parcial_de_formacoes[formacao.tag] += 1

                        #check if the course is able to be connected ####################
                        if idx_formacao_atual in IDXS_PARA_CONEXAO and idx_formacao_atual != 4:
                            #if is able, get the index of the previous course ####################
                            idx_formacao_anterior = IDXS_PARA_CONEXAO[IDXS_PARA_CONEXAO.index(idx_formacao_atual)-1]
                            #add the connection to the dataframe ####################
                            conexoes_entre_universidades = pd.concat([conexoes_entre_universidades, pd.DataFrame([[str(historico.iloc[idx_formacao_anterior+1])+'/'+str(historico.index[idx_formacao_anterior])+'/'+str(historico.iloc[idx_formacao_anterior]), historico.iloc[idx_formacao_atual+1]+'/'+str(historico.index[idx_formacao_atual])+'/'+historico.iloc[idx_formacao_atual]]], columns=['Origem', 'Destino'])], ignore_index=True)

                #check if the university was found ####################
                if universidade_encontrada:
                    #if was found, add the historical to the file ####################
                    historico = historico.to_list()
                    historico[0:0] = [identificador]
                    historicos_handle.writerow(historico)

                    #add the historical in the university to the file ####################
                    historico_na_universidade = historico_na_universidade.to_list()
                    historico_na_universidade[0:0] = [identificador]
                    historico_na_universidade_handle.writerow(historico_na_universidade)

                    #add the total of courses in the university to the file ####################
                    qte_de_formacoes_na_universidade_handle.writerow([identificador, qte_de_formacoes_na_universidade])

                    #get the birth place ####################
                    local_de_nascimento = [root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@CIDADE-NASCIMENTO)'),
                                    root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@UF-NASCIMENTO)'),
                                    root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@PAIS-DE-NASCIMENTO)')]

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

                    #add the connections to the file
                    conexoes_entre_universidades = conexoes_entre_universidades[conexoes_entre_universidades['Origem'].astype(bool)]
                    conexoes_entre_universidades = conexoes_entre_universidades.values.tolist()
                    conexoes_entre_universidades_handle.writerows(conexoes_entre_universidades)

                    #add the total of courses to the series
                    qte_total_de_formacoes = qte_total_de_formacoes + qte_parcial_de_formacoes

                    #add the birth place and the current institution to the file
                    localizacao_handle.writerow(localizacao)

            except  (FileNotFoundError, zipfile.BadZipFile, etree.XMLSyntaxError, KeyError) as e:
                print(f'Error: {e}')
        else:
            break
        print(cont)
        cont += 1

    #add the total of courses to the file
    pd.DataFrame(qte_total_de_formacoes).T.to_csv(f'./results/{OUTPUT}/specific/quantitative/cont_formacoes_total.csv', sep=',', encoding='utf-8', index=False, mode='w')

    #close the files
    localizacao_file.close()
    historicos_file.close()
    historico_na_universidade_file.close()
    qte_de_formacoes_na_universidade_file.close()
    conexoes_entre_universidades_file.close()
