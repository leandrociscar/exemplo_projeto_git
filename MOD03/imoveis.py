# %%
#Importacao de bibliotecas
import requests
from bs4 import BeautifulSoup as bs
import logging
import pandas as pd

# %%
#defino a url de busca já com a pagina como parametro
var_url = 'https://www.vivareal.com.br/venda/sp/sao-paulo/zona-leste/bras/rua-intendencia/apartamento_residencial/?pagina={}'

#%%
#Busca os dados na pagina
i = 1
var_ret = requests.get(var_url.format(i))
soup = bs(var_ret.text)

# %%
#de acordo com analise via google inspect, busco 1 registro
var_apto = soup.find('a',{'class': 'property-card__content-link js-card-title'})
# %%
#visualizo o resultado
print(var_apto)

# %%
#extraio a informacao de total de imoveis
qtd_imoveis = int(soup.find('strong',{'class': 'results-summary__count js-total-records'}).text.replace('.',''))
print(qtd_imoveis)

# %%
#leio cada variável que identifico relevante
var_desc = var_apto.find('span', {'class': 'property-card__title js-cardLink js-card-title'}).text.strip()
print(var_desc)

var_end = var_apto.find('span', {'class': 'property-card__address'}).text.strip()
print(var_end)

var_area = var_apto.find('span', {'class': 'property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area'}).text.strip()
print(var_area)

var_quarto = var_apto.find('li', {'class': 'property-card__detail-item property-card__detail-room js-property-detail-rooms'}).span.text.strip()
print(var_quarto)

var_banheiro = var_apto.find('li', {'class': 'property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom'}).span.text.strip()
print(var_banheiro)

var_vaga  = var_apto.find('li', {'class': 'property-card__detail-item property-card__detail-garage js-property-detail-garages'}).span.text.strip()
print(var_vaga)

var_valor = var_apto.find('div', {'class': 'property-card__price js-property-card-prices js-property-card__price-small'}).text.strip()
print(var_valor)

var_condominio = var_apto.find('strong', {'class': 'js-condo-price'}).text.strip()
print(var_condominio)

var_link = 'https://www.vivareal.com.br' + var_apto['href']
print(var_link)

# %%
#crio um df para armazenar os dados da busca
df = pd.DataFrame(
    columns=[
        'descricao',
        'endereco',
        'area',
        'quartos',
        'banheiro',
        'vaga',
        'valor',
        'condominio',
        '_link'
    ]
)
df.head(1)

# %%
#Armazeno todos os registros da busca em uma variavel
var_aptos = soup.find_all('a',{'class': 'property-card__content-link js-card-title'})

# %%
#faço um loop para escrever no df
i = 0

while qtd_imoveis > df.shape[0]:
    i += 1
    print(f"Valor de i: {i} \t\t qtd_imoveis: {df.shape[0]}")
    ret = requests.get(var_url.format(i))
    soup = bs(ret.text)
    var_aptos = soup.find_all('a',{'class': 'property-card__content-link js-card-title'})
    
    for j in var_aptos:
        try:
            var_desc = j.find('span', {'class': 'property-card__title js-cardLink js-card-title'}).text.strip()
        except:
            var_desc = None
        try:
            var_end = j.find('span', {'class': 'property-card__address'}).text.strip()
        except:
            var_end = None
        try:
            var_area = j.find('span', {'class': 'property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area'}).text.strip()
        except:
            var_area = None
        try:
            var_quarto = j.find('li', {'class': 'property-card__detail-item property-card__detail-room js-property-detail-rooms'}).span.text.strip()
        except:
            var_quarto = None
        try:
            var_banheiro = j.find('li', {'class': 'property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom'}).span.text.strip()
        except:
            var_banheiro = None
        try:
            var_vaga  = j.find('li', {'class': 'property-card__detail-item property-card__detail-garage js-property-detail-garages'}).span.text.strip()
        except:
            var_vaga = None
        try:
            var_valor = j.find('div', {'class': 'property-card__price js-property-card-prices js-property-card__price-small'}).text.strip()
        except:
            var_valor = None
        try:
            var_condominio = j.find('strong', {'class': 'js-condo-price'}).text.strip()
        except:
            var_condominio = None
        try:
            var_link = 'https://www.vivareal.com.br' + j['href']
        except:
            var_link = None

        df.loc[df.shape[0]] = [
            var_desc,
            var_end,
            var_area,
            var_quarto,
            var_banheiro,
            var_vaga,
            var_valor,
            var_condominio,
            var_link
        ]

# %%
#exibo o df
df

# %%
#gero um csv
df.to_csv('bd_imoveis_intendencia.csv', sep=';', index=False)
# %%
