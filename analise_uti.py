from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ARQUIVO_DADOS = Path(__file__).parent / "dados_uti.csv"
PASTA_GRAFICOS = Path(__file__).parent / "graficos"


def carregar_dados(caminho: Path) -> pd.DataFrame:
    """Carrega os dados da UTI e valida as colunas obrigatórias."""
    colunas_obrigatorias = {
        "id_paciente",
        "idade",
        "diagnostico",
        "dias_internacao",
        "ventilacao_mecanica",
        "desfecho",
        "reinternacao",
    }

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    dados = pd.read_csv(caminho)

    colunas_ausentes = colunas_obrigatorias.difference(dados.columns)
    if colunas_ausentes:
        raise ValueError(
            "As seguintes colunas estão ausentes: "
            + ", ".join(sorted(colunas_ausentes))
        )

    return dados


def calcular_indicadores(dados: pd.DataFrame) -> dict:
    """Calcula os principais indicadores do conjunto de dados."""
    total_pacientes = len(dados)
    media_idade = dados["idade"].mean()
    media_permanencia = dados["dias_internacao"].mean()

    taxa_mortalidade = (
        dados["desfecho"].eq("Óbito").mean() * 100
    )

    taxa_ventilacao = (
        dados["ventilacao_mecanica"].eq("Sim").mean() * 100
    )

    taxa_reinternacao = (
        dados["reinternacao"].eq("Sim").mean() * 100
    )

    return {
        "Total de pacientes": total_pacientes,
        "Média de idade": round(media_idade, 1),
        "Média de permanência": round(media_permanencia, 1),
        "Taxa de mortalidade (%)": round(taxa_mortalidade, 1),
        "Uso de ventilação mecânica (%)": round(taxa_ventilacao, 1),
        "Taxa de reinternação (%)": round(taxa_reinternacao, 1),
    }


def exibir_indicadores(indicadores: dict) -> None:
    """Exibe os indicadores de forma organizada no terminal."""
    print("\nANÁLISE DE DADOS DA UTI")
    print("=" * 40)

    for nome, valor in indicadores.items():
        print(f"{nome}: {valor}")

    print("=" * 40)


def criar_grafico_diagnosticos(dados: pd.DataFrame) -> None:
    """Cria gráfico com a quantidade de pacientes por diagnóstico."""
    contagem = dados["diagnostico"].value_counts().sort_values()

    plt.figure(figsize=(10, 6))
    contagem.plot(kind="barh")
    plt.title("Quantidade de pacientes por diagnóstico")
    plt.xlabel("Número de pacientes")
    plt.ylabel("Diagnóstico")
    plt.tight_layout()
    plt.savefig(PASTA_GRAFICOS / "pacientes_por_diagnostico.png")
    plt.close()


def criar_grafico_desfechos(dados: pd.DataFrame) -> None:
    """Cria gráfico com a distribuição dos desfechos."""
    contagem = dados["desfecho"].value_counts()

    plt.figure(figsize=(7, 5))
    contagem.plot(kind="bar")
    plt.title("Distribuição dos desfechos")
    plt.xlabel("Desfecho")
    plt.ylabel("Número de pacientes")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(PASTA_GRAFICOS / "distribuicao_desfechos.png")
    plt.close()


def criar_grafico_permanencia(dados: pd.DataFrame) -> None:
    """Cria histograma dos dias de internação."""
    plt.figure(figsize=(9, 5))
    plt.hist(dados["dias_internacao"], bins=12, edgecolor="black")
    plt.title("Distribuição do tempo de internação")
    plt.xlabel("Dias de internação")
    plt.ylabel("Número de pacientes")
    plt.tight_layout()
    plt.savefig(PASTA_GRAFICOS / "tempo_internacao.png")
    plt.close()


def gerar_relatorio_csv(dados: pd.DataFrame) -> None:
    """Gera um resumo agrupado por diagnóstico."""
    resumo = (
        dados.groupby("diagnostico")
        .agg(
            pacientes=("id_paciente", "count"),
            media_idade=("idade", "mean"),
            media_permanencia=("dias_internacao", "mean"),
            obitos=("desfecho", lambda serie: serie.eq("Óbito").sum()),
        )
        .round(1)
        .sort_values("pacientes", ascending=False)
    )

    resumo.to_csv(
        Path(__file__).parent / "relatorio_por_diagnostico.csv",
        encoding="utf-8-sig",
    )


def main() -> None:
    PASTA_GRAFICOS.mkdir(exist_ok=True)

    dados = carregar_dados(ARQUIVO_DADOS)
    indicadores = calcular_indicadores(dados)

    exibir_indicadores(indicadores)
    criar_grafico_diagnosticos(dados)
    criar_grafico_desfechos(dados)
    criar_grafico_permanencia(dados)
    gerar_relatorio_csv(dados)

    print("\nGráficos e relatório gerados com sucesso.")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as erro:
        print(f"Erro ao executar a análise: {erro}")
