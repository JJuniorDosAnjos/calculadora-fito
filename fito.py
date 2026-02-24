import pandas as pd
import numpy as np

def calcular_fito(df, area_parcela):

    df = df.dropna()

    matriz = pd.crosstab(df["spp"], df["parc"])

    nparc = df["parc"].nunique()

    area_total = area_parcela * nparc

    N = matriz.sum(axis=1)

    DA = N / (area_total / 1000)

    DR = (DA / DA.sum()) * 100

    freq = (matriz > 0).sum(axis=1)

    FA = (freq / nparc) * 100

    FR = (FA / FA.sum()) * 100

    df["areasec"] = (np.pi * df["dap"]**2) / 40000

    DoA = df.groupby("spp")["areasec"].sum() / (area_total / 1000)

    DoR = (DoA / DoA.sum()) * 100

    IVI = DR + FR + DoR

    tabela = pd.DataFrame({
        "N": N,
        "DA": DA,
        "DR": DR,
        "DoA": DoA,
        "DoR": DoR,
        "FA": FA,
        "FR": FR,
        "IVI": IVI
    }).round(4)

    tabela = tabela.sort_values("IVI", ascending=False)

    return tabela
