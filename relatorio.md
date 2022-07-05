---
title: Projeto 2 --- MAC0350
author:
    - Caio Dantas Simão Ugêda, Nº USP:11796868
    - Daniel Pessoa Cardeal, Nº USP:10693170
---
# Analise do tempo de execução das consultas

Para realizar a comparação de performance entre o Postgres e o Neo4j,
adicionamos as palavras-chave `explain analyze` antes da execução das consultas
em questão e observamos os resultados devolvidos. Essas diretivas fazem com que,
além do resultado da consulta, um *log* contendo tempos de execução seja
devolvido. Essa estratégia foi escolhida porque já desconsidera alguns dos
fatores que podem alterar o resultado das execuções mas que são irrelevantes
para nossa análise.

Infelizmente, não vimos um grande ganho de tempo de execução no caso do banco de
dados em grafos comparado ao banco de dados relacional, mas nosso grupo associou
essa diferença em relação ao resultado esperado à fatores como:

- O uso do console *online* para o Neo4j fez com que fosse impossível garantir
  que ambos os testes fossem executados em máquinas iguais.

- O número de graus de indireção é relativamente baixo, o que faz com que a
  perda de performance do modelo relacional possa ser mascarado pelas diversas
  otimizações implementadas no gerenciador Postgres. Esse tipo de otimização
  talvez fosse menos relevante se buscássemos explorar um caso mais extremo,
  como 5 ou 6 graus de indireção.

- O número de instâncias foi relativamente baixo considerando a capacidade das
  máquinas e dos SGBDs.

# Referência dos arquivos

Essa seção explica brevemente o que cada imagem/pasta significa nesse projeto:

1. `imagens/`: pasta contendo todas os registros em imagem das tabelas e
   relações criadas, das quais:

   1. `criacao-neo4j.png`: saída obtida quando adicionamos as entradas à base de
   dados no console online do Neo4j.

   2. `grafo-neo4j.png`: grafo das relações de amizade entre os as diferentes
   pessoas da nossa base de dados, gerada pelo console online do Neo4j.

   3. `postgres-tabelas.png`: diagrama de relações ERD gerado pelo pgadmin.
      Mostra que foram criadas duas relações (`person` e `friendship`) com as
      chaves adequadas.

   4. `postgres-dados.png`: print do console do Postgres mostrando algumas das
      instâncias dos dados gerados.

2. `scripts_sql/`: pasta contendo todos os scripts de geração, manipulação e
   consulta nos respectivos SGBDs.

3. `analises_tempo/`: pasta contendo o tempo de execução das consultas em cada
   um dos SGBDs. Para obter esses dados repetimos a execução da consulta 2.3 no
   Postgres e da consulta 4 no Neo4j adicionando as keywords `explain analyze`
   no começo da consulta. Por exemplo, a consulta em SQL do Postgres ficou:

   ```sql
    explain analyze
    select amigo_am.ID, amigo_am.Name
    from PERSON as alice
    join FRIENDSHIP as f_al on f_al.PersonId = alice.ID
    join FRIENDSHIP as f_am on f_am.PersonId = f_al.FriendId
    join PERSON as amigo_am on amigo_am.ID = f_am.FriendId
    where alice.Name = 'Alice';
   ```
