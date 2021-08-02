#%%
#Importacao de bibliotecas
import requests
import json

#%%
#captura dados da url com o get
url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
var_ret = requests.get(url)

#%%
#vai receber uma das respostas da API sobre o retorno
print(var_ret)

# %%
#a variável com comando get ja trata o IF para 200
if var_ret:
    print(var_ret)
else:
    print('Falhou')

# %%
#mostra em texto o que foi capturado
print(var_ret.text)

# %%
#uso a lib json para visualizar os dados de melhor forma
var_ctc_dol = json.loads(var_ret.text)['USDBRL']
print(var_ctc_dol)

# %%
#agora virou um dicionário
print( f" 20 Dólares hoje custam {float(var_ctc_dol['bid']) * 20} reais")

# %%
#transforma tudo o que foi feito em uma funcao
def calc_cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
    #ou
    #url = 'https://economia.awesomeapi.com.br/json/last/{}'.format(moeda)
    var_ret = requests.get(url)
    var_ctc_dol = json.loads(var_ret.text)[moeda.replace('-','')]
    print( f"{valor} {moeda[:3]} hoje custam {float(var_ctc_dol['bid']) * valor} {moeda[4:]}")

# %%
#Utilizando a funcao
calc_cotacao(20, 'USD-BRL')
calc_cotacao(20, 'JPY-BRL')

# %%
#passar uma chave que nao existe
calc_cotacao(2, 'ciscar')

# %%
#uma das tratativas é o pass, que simplesmente passa em frente caso nao rode
try:
    calc_cotacao(3, 'banana')
except:
    pass

# %%
#caso sucesso dê ok
try:
    calc_cotacao(3, 'USD-BRL')
except:
    pass
else:
    print("ok")

# %%
#exibir o erro do except, retorna o que deu problema
try:
    calc_cotacao(3, 'Ciscar')
except Exception as e:
    print(e)
else:
    print("ok")

# %%
#para deixar claro o exception tento dividir um numero por zero
try:
    1/0
except Exception as e:
    print(e)
else:
    print("ok")

# %%
#criar um decorador de forma manual para resolver a API
#o (func) é que é uma funcao dentro de outra
def error_check(func):
    def inner_func(*args, **kargs):
        try:
            #sao os parametros
            func(*args, **kargs)
        except:
            print(f"{func.__name__} falhou")
    return inner_func

#para o teste de erro ser validado antes da funcao passar
@error_check
def calc_cotacao_c_erro(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
    var_ret = requests.get(url)
    var_ctc_dol = json.loads(var_ret.text)[moeda.replace('-','')]
    print( f"{valor} {moeda[:3]} hoje custam {float(var_ctc_dol['bid']) * valor} {moeda[4:]}")

# %%
#chamadas da funcao com validacao de erro
calc_cotacao_c_erro(20, "USD-BRL")
calc_cotacao_c_erro(20, "PAO-DE-QUEIJO")
calc_cotacao_c_erro(20, "BTC-BRL")

# %%
#para exemplificar melhor os args e kargs, simulo cenarios de conexao do request
import random

def test_func(*args, **kargs):
    rnd= random.random()
    print(f"""
            RDN: {rnd}
            args: {args if args else 'sem args'}
            kargs: {kargs if kargs else 'sem kargs'}
        """)
    if rnd < .2:
        raise ConnectionAbortedError('Conexão foi finalizada')
    elif rnd < .4:
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        raise TimeoutError('Tempo de espera excedido')
    else:
        return "OK!"

# %%
#Testo a funcao sem parametros
test_func()

# %%
#Testo a funcao com args
test_func(2, 4)

# %%
#Testo a funcao com kargs
test_func(x=1)

# %%
#Testo a funcao com args e kargs
test_func(5, 2, x=1)

# %%
#nao é necessario fazer uso de decorador manual, pode usar o backoff
import backoff

# %%
#para o pacote pegar a excecao, escolho os erros que quero expor
#escolho o numero de tentativas maxima
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=2)
def test_func_c_backoff(*args, **kargs):
    rnd= random.random()
    print(f"""
            RDN: {rnd}
            args: {args if args else 'sem args'}
            kargs: {kargs if kargs else 'sem kargs'}
        """)
    if rnd < .2:
        raise ConnectionAbortedError('Conexão foi finalizada')
    elif rnd < .4:
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        raise TimeoutError('Tempo de espera excedido')
    else:
        return "OK!"

# %%
#testo a funcao
test_func_c_backoff()

# %%
#para logs em python temos o pacote logging
import logging

# %%
#pego o resultado do log
log = logging.getLogger()
#defino para ser o log de nível mais baixo
log.setLevel(logging.DEBUG)
#formato o log
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

#crio o canal
#envio para o terminal
ch = logging.StreamHandler()
#defino a formatacao
ch.setFormatter(formatter)
#salvo na log
log.addHandler(ch)


# %%
#edito a funcao para adicionar o log
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=10)
def test_func_c_log(*args, **kargs):
    rnd= random.random()
    log.debug(f" RND: {rnd} ")
    log.info(f"args: {args if args else 'sem args'}")
    log.info(f"kargs: {kargs if kargs else 'sem kargs'}")
    if rnd < .2:
        log.error('Conexão foi finalizada')
        raise ConnectionAbortedError('Conexão foi finalizada')
    elif rnd < .4:
        log.error('Conexão foi recusada')
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        log.error('Tempo de espera excedido')
        raise TimeoutError('Tempo de espera excedido')
    else:
        return "OK!"

# %%
#testo a funcao
test_func_c_log()

# %%
