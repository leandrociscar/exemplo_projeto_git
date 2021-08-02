# %%
#Importacao de bibliotecas
import requests
from bs4 import BeautifulSoup as bs
import logging
import pandas as pd

# %%
#variável da origem do dado
url = 'https://portalcafebrasil.com.br/todos/podcasts/'

# %%
#captura o valor
var_ret = requests.get(url)

# %%
#Exibe o texto extraído
print(var_ret.text)

# %%
#utilizo a biblioteca bs4 beautifulsoup para formatar meu retorno
var_soup = bs(var_ret.text)

# %%
#visualizo o dado tratado, ja fez o parse
var_soup

# %%
#No google inspect analiso a página e identifico o que quero buscar
#identificado que o titulo é no h5, testo se traz o primeiro titulo
var_soup.find('h5').text

# %%
#para trazer o link do título
var_soup.find('h5').a

# %%
#para trazer somente o link limpo
var_soup.find('h5').a['href']

# %%
#para armazenar em uma lista todos os valores
lst_podcast = var_soup.find_all('h5')

# %%
#gero um for para printar os títulos
for i in lst_podcast:
    print(f"EP: {i.text} - Link: {i.a['href']}")


#O resultado nao trouxe todos os registros, isso porque a
#pagina exibe poucos itens até passar o scroll
#analiso entao a aba network do google
#identifico o que acontece de diferente conforme desse scroll
#para esse caso foi um arquivo ajax=true
#o ajax=true indica que está lendo o conteudo de uma outra pagina
#sem carregar a pagina toda

# %%
#defino entao a variavel com o ajax=true para que tem os dados que preciso
#deixo o numero da pagina parametrizavel
var_url = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'

# %%
#crio uma funcao para listar a pagina
def get_podcast(var_url):
    var_ret = requests.get(var_url)
    soup = bs(var_ret.text)
    return soup.find_all('h5')

# %%
#testo a funcao
get_podcast(var_url.format(2))

# %%
#gero o log
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

# %%
#crio um loop para buscar todos os podcasts
i = 1
lst_podcast_full = []
lst_podcast = get_podcast(var_url.format(i))
log.debug(f"Coletado {len(lst_podcast)} do link: {var_url.format(i)}")

while len(lst_podcast) > 0:
    lst_podcast_full = lst_podcast_full + lst_podcast
    i += 1
    lst_podcast = get_podcast(var_url.format(i))
    log.debug(f"Coletado {len(lst_podcast)} do link: {var_url.format(i)}")


# %%
#listo a quantidade de registros que buscou
len(lst_podcast_full)

# %%
#utilizo pandas para criar um df
df = pd.DataFrame(columns=['nome', 'link'])

# %%
#percorro a lista para alimentar o df
for i in lst_podcast_full:
    df.loc[df.shape[0]] = [i.text, i.a['href']]

# %%
#verifico se carregou
df.shape

# %%
#visualizo o resultado
df.head(5)

# %%
#gero um csv com a lista
df.to_csv('banco_podcast.csv', sep=';', index=False)
# %%
