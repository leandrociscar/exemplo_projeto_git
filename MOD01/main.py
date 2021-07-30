#importação de biliotecas
import requests as rqest
import pandas as pd
import collections
import sys

#define a url dos dados a serem coletados
#var_url = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbz8vTxNDRy9_Y2NQ13CDA0sTIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN_FydLAGAgNTKEK8DkRrACPGwpyQyMMMj0VAcySpRM!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K85260Q5OIRSC42046/res/id=historicoHTML/c=cacheLevelPage/=/'

#para capturar a url via chamada no prompt
var_url = sys.argv[1]

#define variável para fazer o request dos dados na url
var_rtrn = rqest.get(var_url)

#converte o resultado para texto e armazena em nova variável
var_rtrn_txt = var_rtrn.text

#converte para df utilizando pandas via read_html
df = pd.read_html(var_rtrn_txt)

#como o resultado foi uma lista, capturo o primeiro objeto da lista e sobreescrevendo o df, gerando um df
df = df[0].copy()

#exibe o df
df

#gero uma lista com 25 números, de 1 a 25
lst_nr_pop = list(range(1,26))
lst_nr_pares = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
lst_nr_impares = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
lst_nr_primos = [2, 3, 5, 7, 11, 13, 17, 19, 23]

#lista combinacao
lst_comb = []
var_01 = 0
var_02 = 0
var_03 = 0
var_04 = 0
var_05 = 0
var_06 = 0
var_07 = 0
var_08 = 0
var_09 = 0
var_10 = 0
var_11 = 0
var_12 = 0
var_13 = 0
var_14 = 0
var_15 = 0
var_16 = 0
var_17 = 0
var_18 = 0
var_19 = 0
var_20 = 0
var_21 = 0
var_22 = 0
var_23 = 0
var_24 = 0
var_25 = 0


#lista campos do DF que serao percorridos
lst_campos_df = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Bola7', 'Bola8','Bola9','Bola10',
                 'Bola11', 'Bola12', 'Bola13', 'Bola14', 'Bola15']

#percorre cada linha do df
for index, row in df.iterrows():
    var_pares = 0
    var_impares = 0
    var_primos = 0
    for i in lst_campos_df:
        if row[i] in lst_nr_pares:
            var_pares += 1
        if row[i] in lst_nr_impares:
            var_impares += 1
        if row[i] in lst_nr_primos:
            var_primos += 1
        if row[i] == 1:
            var_01 += 1
        if row[i] == 2:
            var_02 += 1
        if row[i] == 3:
            var_03 += 1
        if row[i] == 4:
            var_04 += 1
        if row[i] == 5:
            var_05 += 1
        if row[i] == 6:
            var_06 += 1
        if row[i] == 7:
            var_07 += 1
        if row[i] == 8:
            var_08 += 1
        if row[i] == 9:
            var_09 += 1
        if row[i] == 10:
            var_10 += 1
        if row[i] == 11:
            var_11 += 1
        if row[i] == 12:
            var_12 += 1
        if row[i] == 13:
            var_13 += 1
        if row[i] == 14:
            var_14 += 1
        if row[i] == 15:
            var_15 += 1
        if row[i] == 16:
            var_16 += 1
        if row[i] == 17:
            var_17 += 1
        if row[i] == 18:
            var_18 += 1
        if row[i] == 19:
            var_19 += 1
        if row[i] == 20:
            var_20 += 1
        if row[i] == 21:
            var_21 += 1
        if row[i] == 22:
            var_22 += 1
        if row[i] == 23:
            var_23 += 1
        if row[i] == 24:
            var_24 += 1
        if row[i] == 25:
            var_25 += 1
    lst_comb.append(str(var_pares) + 'p-' + str(var_impares) + 'i-' + str(var_primos) + 'np')

#armazena o resultado da qtde dos numeros sorteados
freq_nr = [
    [1, var_01],
    [2, var_02],
    [3, var_03],
    [4, var_04],
    [5, var_05],
    [6, var_06],
    [7, var_07],
    [8, var_08],
    [9, var_09],
    [10, var_10],
    [11, var_11],
    [12, var_12],
    [13, var_13],
    [14, var_14],
    [15, var_15],
    [16, var_16],
    [17, var_17],
    [18, var_18],
    [19, var_19],
    [20, var_20],
    [21, var_21],
    [22, var_22],
    [23, var_23],
    [24, var_24],
    [25, var_25]
]

#exibe o reusltado
freq_nr

#ordena pela variável de quantidade
freq_nr.sort(key=lambda tup: tup[1])

#o numero que mais saiu
freq_nr[0]

#o numero que menos saiu
freq_nr[-1]

#gero uma colecao da combinacao gerada inicialmente para saber quantas vezes caiu cada combinacao
contador = collections.Counter(lst_comb)
contador

#converte para um df
df_rslt = pd.DataFrame(contador.items(), columns=['Combinacao', 'Frequencia'])
df_rslt

#gero uma coluna com o pct da frequenciae ordeno
df_rslt['p_freq'] = df_rslt['Frequencia']/df_rslt['Frequencia'].sum()
df_rslt = df_rslt.sort_values(by='p_freq')
df_rslt

#gero um print com os resultados
print('''

O número mais frequente é o: {}
O número menos frequente é o: {}
A combinação de Pares, Impares e Primos mais frequente é: {} com a frequencia de: {}%
'''.format(freq_nr[-1][0], freq_nr[00][0], df_rslt['Combinacao'].values[-1], int((df_rslt['p_freq'].values[-1]*100)*100)/100)
)


