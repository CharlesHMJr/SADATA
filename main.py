import io
import zipfile

import string
import glob
import csv
from lxml import etree

inicio = int(input('Informe o início: '))
fim = int(input('Informe o fim: '))
curriculos = glob.glob('collection/*/*')
cont = 0

cidades = csv.writer(open('cidades.csv', 'w', newline=''))
header = ['Cidade', 'Qte de Academicos']
cidades.writerow(header)
cidade_nascimento, qte_nascimento = [], []

amostras = csv.writer(open('amostras.csv', 'w', newline=''))
header = ['Identificador', 'Nome', 'Cidade']
amostras.writerow(header)

for curriculo in curriculos:
    CFT = False
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
            orcid = root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@ORCID-ID)')

            print(f'{identificador}: {nome}')

            formacoes = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/*')
            nascimento = string.capwords(root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@CIDADE-NASCIMENTO)'))
            
            for formacao in formacoes:
                try:
                    if formacao.xpath('string(@NOME-INSTITUICAO)')=='Centro Federal de Educação Tecnológica de Minas Gerais':
                        CFT = True
                        break
                except:
                    pass

            if CFT:
                amostras.writerow([identificador, nome, nascimento])
                if nascimento not in cidade_nascimento:
                    cidade_nascimento.append(nascimento)
                    qte_nascimento.append(1)
                else:
                    qte_nascimento[cidade_nascimento.index(nascimento)] += 1
            
            print(cidade_nascimento, qte_nascimento)

        except:
            pass
    cont += 1

data = zip(tuple(cidade_nascimento), tuple(qte_nascimento))
cidades.writerows(data)
