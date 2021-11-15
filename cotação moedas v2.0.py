import requests
import pandas as pd
from datetime import datetime

# Referencia a data inicial.
#Data_inicio=int(input('data inicial **YYYYMMDD** '))
Data_inicio=20200101
# Referencia a data final.
#Data_final=int(input('data final **YYYYMMDD** '))
Data_final=20200131
# Retorna a quantidade de dias pesquisados.
Qtd_dias = (Data_final-Data_inicio)+1
#Contador
Dias = []
for i in range(0,Qtd_dias):
 #Dias.append(Data_inicio+i)
   Dias.append(str(Data_inicio+i))

for i, v in enumerate(Dias):
  Dias[i] = datetime.strptime(v, '%Y%m%d').strftime('%d/%m/%Y')

Bandeira=[]

#Lista de Moedas.
Moedas=['EUR-BRL','USD-BRL','GBP-BRL']

for m in Moedas:
  if m == 'USD-BRL':
    Bandeira.append("DOLAR")
  elif m == 'EUR-BRL':
    Bandeira.append("EURO")
  elif m == 'GBP-BRL':
    Bandeira.append("LIBRA ESTERLINA")
  else:
    Bandeira.append('MOEDA N.I') 
  # pesquisa os dias selecionados
  requisicao = requests.get(f'https://economia.awesomeapi.com.br/{m}/{Qtd_dias}?start_date={Data_inicio}&end_date={Data_final}')

  # Cria um dicionario dos itens pesquisados.
  requisicao_dic = requisicao.json()

  #Colunas

  C_Data = Dias.copy()
  C_Compra = []
  C_Venda = []

  for v in range(len(requisicao_dic)):
    C_Compra.append(requisicao_dic[v]['bid'])

  for v in range(len(requisicao_dic)):
    C_Venda.append(requisicao_dic[v]['ask'])

  # Dicionario nulo para criar as cotações.

  Cotacao_dic = {}

  #Adicionando Cotações dentro do Dicionario.

  Cotacao_dic["Data"] = C_Data.copy()
  Cotacao_dic["Compra"] = C_Compra.copy()
  Cotacao_dic["Venda"] = C_Venda.copy()

  Contador= Bandeira.copy()*(len(Dias))

  Cotacao_dic["Moeda"] =(Contador.copy())

  #Limpeza das variaves para o proximo for. 
  Contador.clear()
  C_Data.clear()
  C_Compra.clear()
  C_Venda.clear()
  
  #datatoexcel = pd.ExcelWriter(f'{Bandeira}_{Data_inicio}_{Data_final}.xlsx',index=False)

  print(Cotacao_dic)

  tabela = pd.DataFrame(Cotacao_dic)
  tabela[["Compra", "Venda"]] = tabela[["Compra", "Venda"]].apply(pd.to_numeric)

  if m == 'USD-BRL':
    tabela.to_excel(f'DOLAR_{Data_inicio}_{Data_final}.xlsx', index=False)
  elif m == 'EUR-BRL':
    tabela.to_excel(f'EURO_{Data_inicio}_{Data_final}.xlsx', index=False)
  elif m == 'GBP-BRL':
    tabela.to_excel(f'LIBRA_ESTERLINA_{Data_inicio}_{Data_final}.xlsx', index=False)
  else:
    tabela.to_excel(f'MOEDA_N.I_{Data_inicio}_{Data_final}.xlsx', index=False) 

  #datatoexcel.save()
  Bandeira.clear()

print(f"Cotação Atualizada. {datetime.now()}")