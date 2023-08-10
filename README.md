![](/img/banner_curry_go.jpg)

# 1. Problema de Negócio
A Curry.Go é uma empresa de tecnologia que criou um aplicativo que conecta restaurantes, entregadores e pessoas em um marketplace.

Através deste aplicativo é possível realizar o pedido de uma refeição, em qualquer um dos restaurantes cadastrados, e recebê-lo no conforto da sua casa por um entregador também cadastrado no aplicativo da Curry.Go.

Desta maneira, a empresa realiza negócios entre restaurantes, entregadores e pessoas, e gera muitos dados sobre entregas, tipos de pedidos, condições climáticas, avaliação dos entregadores e etc. Apesar da entrega estar crescendo, em números brutos, o CEO não tem visibilidade completa dos KPIs de crescimento da empresa.

Você foi contratado como um Cientista de Dados para criar soluções de dados para entrega, mas antes de treinar algoritmos, a necessidade da empresa é ter os principais KPIs estratégicos organizados em uma única ferramenta, para que possa consultar e conseguir tomar decisões simples, porém de extrema importância.

A Curry.Go Company possui um modelo de negócio chamado de Marketplace, que faz o intermédio do negócio entre três clientes principais: restaurantes, entregadores e compradores. Para acompanhar o crescimento desses negócios, o CEO gostaria de visualizar as seguintes métricas de crescimento:

## Do ponto de vista da Empresa:
1. Quantidade de pedidos por dia.
2. Quantidade de pedidos por semana.
3. Distribuição dos pedidos por tipo de tráfego.
4. Comparação do volume de pedidos por cidade e tipo de tráfego.
5. A quantidade de pedidos por entregador por semana.
6. A localização central de cada cidade por tipo de tráfego.

## Do ponto de vista dos Entregadores:
1. A menor e a maior idade dos entregadores.
2. A pior e a melhor condição dos veículos.
3. A avaliação média por entregador.
4. A avaliação média e o desvio padrão por tipo de tráfego.
5. A avaliação média e o desvio padrão por condições climáticas.
6. Os 10 entregadores mais rápidos por cidade.
7. Os 10 entregadores mais lentos por cidade.

## Do ponto de vista dos Restaurantes:
1. A quantidade de entregadores únicos.
2. A distância média dos restaurantes e dos locais de entrega.
3. O tempo médio e o desvio padrão de entrega por cidade.
4. O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido.
5. O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.
6. O tempo médio de entrega durante os Festivais.

O objetivo deste projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor maneira possível para o CEO.


# 2. Premissas assumidas para a análise do Negócio
1. A Análise foi realizada com dados entre 11/02/2022 e 06/04/2022.
2. O modelo de negócio assumido foi o de um Marketplace.
3. As três principais visões do negócio foram: visão empresa (transação de pedidos), visão restaurante e visão entregadores.


# 3. Planejamento da solução
O painel estratégico foi desenvolvido utilizando métricas que refletem as três visões do modelo de negócio:
### Visão do crescimento da empresa
  1. Pedidos por dia
  2. Porcentagem de pedidos por condições de trânsito
  3. Quantidade de pedidos por tipo e por cidade
  4. Pedidos por semana
  5. Quantidade de pedidos por tipo de entrega.
  6. Quantidade de pedidos por condições de trânsito e tipo de cidade
### Visão do crescimento dos entregadores
  1. Idade do entregador mais velho, do mais novo e a média de idade.
  2. Avaliação do melhor e do pior veículo.
  3. Avaliação média por entregador.
  4. Avaliação média por condições de trânsito.
  5. Avaliação média por condições climáticas.
  6. Tempo médio do entregador mais rápido por cidade.
  7. Tempo médio do entregador mais lento por cidade.
### Visão do crescimento dos restaurantes
  1. Quantidade de pedidos únicos
  2. Distância média percorrida
  3. Tempo médio de entrega durante festival e dias normais. 
  4. Desvio padrão do tempo de entrega durante festival e dias normais.
  5. Tempo de entrega médio por cidade
  6. Distribuição do tempo médio de entrega por cidade.
  7. Tempo médio de entrega por tipo de pedido.


# 4. Os 3 principais insights de negócio através dos dados
1. A sazonalidade da quantidade de pedidos é diária; há uma variação de aproximadamente 10% do número de pedidos em dias subsequentes.
2. As cidades do tipo Semi-Urban não possuem condição de trânsito baixa ("Low").
3. As entregas em condições climáticas de sol ("Sunny") possuem média mais alta das avaliações, porém possuem uma maior dispersão entre as avaliações (uma maior diferença entre as avaliações mais baixas e as mais altas).


# 5. Produto final do projeto
Painel online, hospedado em uma Cloud e disponível para acesso em qualquer dispositivo conectado à internet.
O painel pode ser acessado através deste link: https://cristhofer-weiland-curry-go-company-project.streamlit.app/


# 6. Conclusão
Tendo como objetivo deste projeto a criação de um conjunto de gráficos e/ou tabelas que exibam as métricas da melhor maneira possível para o CEO, podemos concluir que o objetivo foi alcançado.
- Da visão da empresa, conclui-se que o número de pedidos cresceu entre as semanas 06 e 13 do ano de 2022.
- Da visão dos entregadores, buscamos apresentar também a média de idade destes: 29,6 anos.
- Da visão dos restaurantes, foram 1320 entregadores únicos no período da análise que percorreram uma distância média por entrega de 27,35 KM com um tempo médio de 26,16 minutos.


# 7. Próximos passos
Dentre alguns dos pontos que poderiam ser tratados em uma eventual melhoria deste projeto estão:
1. Reduzir o número de métricas.
2. Criar novos filtros.
3. Adicionar outras visões de negócio.