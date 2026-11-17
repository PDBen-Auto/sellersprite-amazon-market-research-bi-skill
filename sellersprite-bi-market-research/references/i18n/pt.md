# Pesquisa de mercado SellerSprite e BI

`sellersprite-bi-market-research` · Português

## Objetivo e âmbito

Expandir a intenção inicial para ASIN relevantes, separar camadas e criar BI auditável deduplicado por ASIN-pai.

## Fundamento e dependências

Mercado/tarefa definidos, XLSX padrão/detalhado e palavras-chave necessárias, Python 3/openpyxl. Online exige conta/navegador SellerSprite autorizados. Estimativas não são liquidações Amazon.

## Entradas

Âmbito/data/mercado/inclusão-exclusão, seed_keyword/seed_asins para descoberta; exportações condicionais; regras/atributos/destinos opcionais. Nenhuma credencial.

## Saídas

Manifest de candidatos com razões/cobertura detalhada; pai/mês/ano/YTD/períodos/receita de marca/momentum; dashboard.html autónomo, auditoria e lacunas.

## Procedimento

1. Fixar tarefa
2. agrupar palavras e core_direct/adjacent_substitute/excluded_noise/review
3. rever pendentes/exclusões elevadas
4. denominador só com aceites e detalhe
5. deduplicar pai/mês sem somar variantes
6. separar unidades/receita/GMV modelado/meses iguais
7. ranking global fixo, momentum distinto de oportunidades
8. conferir números/filtros/imagens/páginas.

## Limites e condições de interrupção

Amostra de pesquisa não é TAM. Sem detalhe não há histórico; sem receita, marca/ranking N/A. Desconhecido≠0. Separar US/CA/MX. Não contornar acesso; ranking por receita amostral, não Amazon BSR.

## Exemplo de pedido

Use `$sellersprite-bi-market-research` — Criar BI do mercado direto a partir de palavras/concorrentes sem incluir candidatos sem detalhe no denominador de vendas; responda em português e preserve as provas, os dados desconhecidos e os limites de autorização.

## Especificação completa

[Entrada do Skill e referências detalhadas](../../SKILL.md).

Use o idioma explicitamente solicitado; caso contrário, siga o idioma do pedido. Preserve comandos, identificadores, chaves JSON, valores enumerados, unidades e citações originais. Distinga traduções e originais. Não deduza país, moeda ou jurisdição pelo idioma. Leia as referências detalhadas relevantes e mantenha todas as verificações e autorizações existentes.

Antes da entrega, confira entradas, provas, valores em falta, ficheiros e critérios de conclusão originais. Assinale como não verificados os passos não executados; o sucesso de um script não valida conclusões comerciais.

## Cobertura linguística e validação

Este guia localizado cobre objetivo, requisitos, entradas, saídas, passos, exemplos e limites; não traduz todas as referências linha por linha. Referências técnicas detalhadas, casos históricos, erros de scripts, interfaces de exemplo e imagens mantêm o idioma original e podem ser explicados a pedido. Verificam-se estrutura, ligações e restrições essenciais; não se afirma revisão por falantes nativos de cada idioma.

