# Análise de Dados de UTI com Python

Projeto de portfólio desenvolvido para praticar análise de dados com Python, utilizando um conjunto de dados fictício de pacientes internados em uma Unidade de Terapia Intensiva.

## Objetivo

O objetivo do projeto é transformar dados hospitalares em indicadores simples e úteis, como:

- número total de pacientes;
- média de idade;
- tempo médio de internação;
- taxa de mortalidade;
- uso de ventilação mecânica;
- taxa de reinternação;
- distribuição dos diagnósticos.

## Tecnologias utilizadas

- Python
- Pandas
- Matplotlib
- Git e GitHub

## Estrutura do projeto

```text
portfolio_analise_uti/
├── analise_uti.py
├── dados_uti.csv
├── requirements.txt
├── .gitignore
└── README.md
```

Após a execução, o projeto também cria:

```text
graficos/
├── distribuicao_desfechos.png
├── pacientes_por_diagnostico.png
└── tempo_internacao.png

relatorio_por_diagnostico.csv
```

## Como executar

1. Clone este repositório:

```bash
git clone URL_DO_SEU_REPOSITORIO
```

2. Entre na pasta:

```bash
cd portfolio_analise_uti
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o projeto:

```bash
python analise_uti.py
```

## Sobre os dados

Os dados utilizados neste projeto são totalmente fictícios e foram criados apenas para fins educacionais. Nenhuma informação real de pacientes foi utilizada.

## Principais aprendizados

Com este projeto, pratiquei:

- leitura de arquivos CSV;
- validação de dados;
- criação de funções em Python;
- cálculos de indicadores;
- agrupamento de dados com Pandas;
- criação de gráficos com Matplotlib;
- geração de relatórios;
- organização de um projeto para publicação no GitHub.

## Próximas melhorias

- criar filtros por faixa etária;
- comparar pacientes com e sem ventilação mecânica;
- criar um dashboard no Power BI;
- adicionar testes automatizados;
- criar uma versão interativa com Streamlit.

## Autora

Daniela Caires

Profissional em transição para Tecnologia, com interesse em Inteligência Artificial, Dados, Qualidade e Automação.
