#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd

def data_counter():
    OUTPUT = 'new'
    ANALISE_ESPECIFICA = False
    if ANALISE_ESPECIFICA:
        DIR = f'./results/{OUTPUT}/specific'
    else:
        DIR = f'./results/{OUTPUT}/general'

    #get the historical data ####################
    historicos = pd.read_csv(f'{DIR}/primary/historicos.csv', sep=',')

    #count the education based on start ####################
    qte_formacoes_iniciadas = historicos.value_counts(['CURSO-TECNICO-PROFISSIONALIZANTE', 'Início.1'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()
    qte_formacoes_iniciadas = pd.concat([qte_formacoes_iniciadas, historicos.value_counts(['GRADUACAO', 'Início.2'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()], axis=1)
    qte_formacoes_iniciadas = pd.concat([qte_formacoes_iniciadas, historicos.value_counts(['MESTRADO', 'Início.4'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()], axis=1)
    qte_formacoes_iniciadas = pd.concat([qte_formacoes_iniciadas, historicos.value_counts(['DOUTORADO', 'Início.5'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()], axis=1)
    #create a csv file with the data ####################
    qte_formacoes_iniciadas.to_csv(f'{DIR}/quantitative/cont_historicos_iniciados.csv', sep=',', encoding='utf-8', index=False)

    #count the education based on end ####################
    qte_formacoes_concluidas = historicos.value_counts(['CURSO-TECNICO-PROFISSIONALIZANTE', 'Fim.1']).to_frame('Quantidade').reset_index()
    qte_formacoes_concluidas = pd.concat([qte_formacoes_concluidas, historicos.value_counts(['GRADUACAO', 'Fim.2']).to_frame('Quantidade').reset_index()], axis=1)
    qte_formacoes_concluidas = pd.concat([qte_formacoes_concluidas, historicos.value_counts(['MESTRADO', 'Fim.4']).to_frame('Quantidade').reset_index()], axis=1)
    qte_formacoes_concluidas = pd.concat([qte_formacoes_concluidas, historicos.value_counts(['DOUTORADO', 'Fim.5']).to_frame('Quantidade').reset_index()], axis=1)
    #create a csv file with the data ####################
    qte_formacoes_concluidas.to_csv(f'{DIR}/quantitative/cont_historicos_finalizados.csv', sep=',', encoding='utf-8', index=False)

    #check if the analysis is from a specific university ####################
    if ANALISE_ESPECIFICA:
        #if it is, get the historical data from the university ####################
        historicos_na_universidade = pd.read_csv(f'{DIR}/primary/cont_historicos_na_universidade.csv', sep=',')

        #count the education in the university based on start ####################
        qte_formacoes_iniciadas_na_universidade = historicos_na_universidade.value_counts(['CURSO-TECNICO-PROFISSIONALIZANTE', 'Início.1'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()
        qte_formacoes_iniciadas_na_universidade = pd.concat([qte_formacoes_iniciadas_na_universidade, historicos_na_universidade.value_counts(['GRADUACAO', 'Início.2'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()], axis=1)
        qte_formacoes_iniciadas_na_universidade = pd.concat([qte_formacoes_iniciadas_na_universidade, historicos_na_universidade.value_counts(['MESTRADO', 'Início.4'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()], axis=1)
        qte_formacoes_iniciadas_na_universidade = pd.concat([qte_formacoes_iniciadas_na_universidade, historicos_na_universidade.value_counts(['DOUTORADO', 'Início.5'.encode('utf-8').decode('utf-8')]).to_frame('Quantidade').reset_index()], axis=1)
        #create a csv file with the data ####################
        qte_formacoes_iniciadas_na_universidade.to_csv(f'{DIR}/quantitative/cont_historicos_na_universidade_iniciados.csv', sep=',', encoding='utf-8', index=False)

        #count the education in the university based on end ####################
        qte_formacoes_concluidas_na_universidade = historicos_na_universidade.value_counts(['CURSO-TECNICO-PROFISSIONALIZANTE', 'Fim.1']).to_frame('Quantidade').reset_index()
        qte_formacoes_concluidas_na_universidade = pd.concat([qte_formacoes_concluidas_na_universidade, historicos_na_universidade.value_counts(['GRADUACAO', 'Fim.2']).to_frame('Quantidade').reset_index()], axis=1)
        qte_formacoes_concluidas_na_universidade = pd.concat([qte_formacoes_concluidas_na_universidade, historicos_na_universidade.value_counts(['MESTRADO', 'Fim.4']).to_frame('Quantidade').reset_index()], axis=1)
        qte_formacoes_concluidas_na_universidade = pd.concat([qte_formacoes_concluidas_na_universidade, historicos_na_universidade.value_counts(['DOUTORADO', 'Fim.5']).to_frame('Quantidade').reset_index()], axis=1)
        #create a csv file with the data ####################
        qte_formacoes_concluidas_na_universidade.to_csv(f'{DIR}/quantitative/cont_historicos_na_universidade_finalizados.csv', sep=',', encoding='utf-8', index=False)

    #get the birth places and current institutions ####################
    localizacao = pd.read_csv(f'{DIR}/primary/localizacao.csv', sep=',')

    #count the birth places ####################
    qte_local_de_nascimento = localizacao.value_counts(['Cidade de Origem', 'Estado de Origem']).to_frame('Quantidade')
    qte_local_de_nascimento.to_csv(f'{DIR}/quantitative/cont_localizacao_de_nascimento.csv', sep=',', encoding='utf-8')

    #count the current institutions ####################
    qte_local_de_atuacao = localizacao.value_counts(['Cidade de Atuação', 'Estado de Atuação']).to_frame('Quantidade')
    qte_local_de_atuacao.to_csv(f'{DIR}/quantitative/cont_localizacao_de_atuacao.csv', sep=',', encoding='utf-8')

    #get the fields of research ####################
    areas_de_atuacao = pd.read_csv(f'{DIR}/primary/areas_de_atuacao.csv', sep=',')

    #count the fields of research ####################
    qte_areas_de_atuacao = areas_de_atuacao.value_counts(['Grande Área','Área']).to_frame('Quantidade')
    qte_areas_de_atuacao.to_csv(f'{DIR}/quantitative/cont_areas_de_atuacao.csv', sep=',', encoding='utf-8')
