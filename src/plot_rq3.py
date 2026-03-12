import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = Path("img/RQ3")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RQ = "RQ3"

df_long = pd.read_csv(DATA_DIR / "respostas_long.csv")
sub = df_long[df_long["RQ"] == RQ].copy()
sub["Categoria"] = sub["Categoria"].replace({"Diagnóstico/Cause-raiz": "Diagnóstico/Causa-raiz"})
counts = sub["Categoria"].value_counts()

MIN_COUNT = 4
main = counts[counts >= MIN_COUNT]
others = counts[counts < MIN_COUNT].sum()
counts_grouped = main.copy()
if others > 0:
    counts_grouped.loc["Outros"] = others

counts_sorted = counts_grouped.sort_values()


#Gráfico 1: Barras horizontais
plt.figure(figsize=(10, 6))
bars = plt.barh(counts_sorted.index, counts_sorted.values)

plt.xlabel("Ocorrências (menções)")
plt.title(f"{RQ} — Tipos de suporte à decisão (ocorrências)")

max_val = counts_sorted.max()
x_pad = max(1, int(max_val * 0.02))

for bar in bars:
    w = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    plt.text(w + x_pad, y, f"{int(w)}", va="center")

plt.xlim(0, max_val + 6 * x_pad)
plt.tight_layout()
plt.subplots_adjust(left=0.45)

out_path1 = OUT_DIR / f"{RQ}_barras.png"
plt.savefig(out_path1, dpi=300)
plt.show()
print(f"Salvo em: {out_path1}")


#Gráfico 2: Heatmap de coocorrência
df_clean = pd.read_csv(DATA_DIR / "respostas_clean.csv")

rq3 = df_clean[["Título", "RQ3"]].copy()
rq3["RQ3"] = rq3["RQ3"].fillna("").astype(str)
rq3["RQ3"] = rq3["RQ3"].str.replace("Diagnóstico/Cause-raiz", "Diagnóstico/Causa-raiz", regex=False)

rq3["RQ3"] = rq3["RQ3"].apply(lambda s: [x.strip() for x in s.split("+") if x.strip()])
rq3 = rq3.explode("RQ3").rename(columns={"RQ3": "Categoria"})
rq3 = rq3.dropna(subset=["Categoria"])

keep = set(main.index)
rq3["Categoria"] = rq3["Categoria"].apply(lambda x: x if x in keep else "Outros")

rq3 = rq3.drop_duplicates(["Título", "Categoria"])

mat = pd.crosstab(rq3["Título"], rq3["Categoria"])
co = mat.T.dot(mat)

plt.figure(figsize=(10, 8))
plt.imshow(co.values, aspect="auto")
plt.xticks(range(len(co.columns)), co.columns, rotation=45, ha="right")
plt.yticks(range(len(co.index)), co.index)
plt.title(f"{RQ} — Coocorrência de tipos de suporte (por paper)")
plt.colorbar(label="Nº de papers com ambas as categorias")
plt.tight_layout()

out_path2 = OUT_DIR / f"{RQ}_heatmap.png"
plt.savefig(out_path2, dpi=300)
plt.show()
print(f"Salvo em: {out_path2}")