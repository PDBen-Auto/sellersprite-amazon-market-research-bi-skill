# Pesquisa de mercado SellerSprite e BI

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Use o idioma explicitamente solicitado; caso contrário, siga o idioma do pedido. Preserve comandos, identificadores, chaves JSON, valores enumerados, unidades e citações originais. Distinga traduções e originais. Não deduza país, moeda ou jurisdição pelo idioma. Leia as referências detalhadas relevantes e mantenha todas as verificações e autorizações existentes.

## Instalação e utilização

Transfira ou clone o repositório e copie o diretório do Skill indicado, com as suas references, scripts, assets e demais dependências existentes, para o diretório de Skills do ambiente. Preserve o nome e SKILL.md. Mudar o idioma da documentação não exige outra instalação. Os comandos são opções, não provas de instalação ou ativação.

```sh
git clone https://github.com/PDBen-Auto/sellersprite-amazon-market-research-bi-skill.git
```

## Pesquisa de mercado SellerSprite e BI

`sellersprite-bi-market-research`

Expandir a intenção inicial para ASIN relevantes, separar camadas e criar BI auditável deduplicado por ASIN-pai.

Diretório do Skill: `.`

**Fundamento e dependências**

Mercado/tarefa definidos, XLSX padrão/detalhado e palavras-chave necessárias, Python 3/openpyxl. Online exige conta/navegador SellerSprite autorizados. Estimativas não são liquidações Amazon.

**Entradas**

Âmbito/data/mercado/inclusão-exclusão, seed_keyword/seed_asins para descoberta; exportações condicionais; regras/atributos/destinos opcionais. Nenhuma credencial.

**Saídas**

Manifest de candidatos com razões/cobertura detalhada; pai/mês/ano/YTD/períodos/receita de marca/momentum; dashboard.html autónomo, auditoria e lacunas.

[Procedimento · Limites e condições de interrupção · Exemplo de pedido](references/i18n/pt.md)

> Use `$sellersprite-bi-market-research` — Criar BI do mercado direto a partir de palavras/concorrentes sem incluir candidatos sem detalhe no denominador de vendas; responda em português e preserve as provas, os dados desconhecidos e os limites de autorização.

## Cobertura linguística e validação

Este guia localizado cobre objetivo, requisitos, entradas, saídas, passos, exemplos e limites; não traduz todas as referências linha por linha. Referências técnicas detalhadas, casos históricos, erros de scripts, interfaces de exemplo e imagens mantêm o idioma original e podem ser explicados a pedido. Verificam-se estrutura, ligações e restrições essenciais; não se afirma revisão por falantes nativos de cada idioma.

Antes da entrega, confira entradas, provas, valores em falta, ficheiros e critérios de conclusão originais. Assinale como não verificados os passos não executados; o sucesso de um script não valida conclusões comerciais.
