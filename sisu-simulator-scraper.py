"""Visita todos os campi de um determinado curso no site SisuSimulator, calcula
a média ponderada com base nos pesos do curso na edição de 2020 do SiSU, retorna
a diferença entre a média do usuário e a nota de corte da ampla concorrência em 2020
e salva o resultado num arquivo .txt"""

import requests
from bs4 import BeautifulSoup
import re

def busca_links(soup):
    divs = soup.find_all("div", class_="col-sm-6 col-xs-12 result")
    arquivo = open("sisu-simulator2020.txt","w")
    for div in divs:
        link = div.a['href']
        resultado = busca_uni(link)
        arquivo.write(resultado + "\n")
    arquivo.close()

def busca_uni(link):
    link_completo = "https://sisusimulator.com.br" + str(link)
    uni_dados = requests.get(link_completo)
    uni_soup = BeautifulSoup(uni_dados.text, 'html.parser')
    resultado = encontra_nota(uni_soup)
    return resultado

def encontra_nota(soup):
    title = soup.find_all("title")
    nome_completo = title[0].string
    uni_nome = re.search('\(([^)]+)', str(nome_completo)).group(1)
    resultado = uni_nome + ": não informada"

    final = nota_pesos(soup)
    if final == 0:
        return resultado
    
    linhas = soup.find_all("tr", class_="notasCorte1 2020_1-1")
    for linha in linhas:
        if linha.td.string == "Ampla concorrência":
            nota_corte = float(linha.span.string)
            diferenca = round((final - nota_corte), 2)
            resultado = uni_nome + ": " + str(diferenca)
    print(resultado)
    return resultado

def nota_pesos(soup):
    notas = [663.5, 766, 741.5, 631.7, 960] # Disciplinas: L, M, CH, CN, R
    soma_notas = 0
    final = 0
    soma_pesos = 0
    pesos = soup.find_all(attrs={"data-type": "peso"})
    
    index = 0
    try:
        for peso in pesos:
            p = float(peso.string)
            soma_pesos += p
            nota_p = notas[index] * p
            soma_notas += nota_p
            index += 1
    except IndexError:
        """print("Não foi possível calcular esta nota.")"""

    if soma_pesos == 0:
        return final
    else:
        final = soma_notas / soma_pesos
        return final

pagina = "https://sisusimulator.com.br/curso/geologia"
dados = requests.get(pagina)
soup = BeautifulSoup(dados.text, 'html.parser')
busca_links(soup)
