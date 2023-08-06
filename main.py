import io
import zipfile

import string
import glob
import pandas as pd
from lxml import etree

inicio = int(input('Informe o início: '))
fim = int(input('Informe o fim: '))
curriculos = glob.glob('collection/*/*')
cont = 0

amostras = pd.DataFrame(columns=['Identificador', 'Nome', 'Cidade'])

for curriculo in curriculos:
    if int(inicio)-1 <= int(cont) < int(fim):
        try:
            arquivo_handle = open(curriculo, 'rb')
            content = arquivo_handle.read()
            if curriculo.split('.')[-1] == 'zip':
                # se nao for bytes, converte
                if type(content) == type(str):
                    content = content.encode('utf-8')
                zip_memory = io.BytesIO(content)
				# abre o zip
                zip_data = zipfile.ZipFile(zip_memory)
                xml = b''
				# le o curriculo
                for fn in zip_data.namelist():
                    xml += zip_data.read(fn)
                content = xml

            root = etree.XML(content)
            identificador = root.xpath('string(/CURRICULO-VITAE/@NUMERO-IDENTIFICADOR)')
            nome = root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@NOME-COMPLETO)')
            nome = nome.encode('utf-8').decode('utf-8')

            print(f'{identificador}: {nome}')

            formacoes = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/*')
            nascimento = string.capwords(root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@CIDADE-NASCIMENTO)'))
            
            for formacao in formacoes:
                try:
                    if formacao.xpath('string(@NOME-INSTITUICAO)')=='Centro Federal de Educação Tecnológica de Minas Gerais':
                        amostras = pd.concat([pd.DataFrame([[identificador, nome, nascimento]], columns=amostras.columns), amostras], ignore_index=True)
                        break
                except:
                    pass

        except:
            pass
    cont += 1

amostras.to_csv('amostras.csv', sep='\t')
amostras.value_counts('Cidade').to_csv('cidades.csv', sep='\t')