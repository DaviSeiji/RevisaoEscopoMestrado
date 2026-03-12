import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = Path("img/RQ8")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RQ = "RQ8"

#Gráfico 1: Barras horizontais
df_long = pd.read_csv(DATA_DIR / "respostas_long.csv")
sub = df_long[df_long["RQ"] == RQ].copy()

counts = sub["Categoria"].value_counts()

MIN_COUNT = 3
main = counts[counts >= MIN_COUNT]
others = counts[counts < MIN_COUNT].sum()
counts_grouped = main.copy()
if others > 0:
    counts_grouped.loc["Outros"] = others

counts_sorted = counts_grouped.sort_values()

plt.figure(figsize=(10, 6))
bars = plt.barh(counts_sorted.index, counts_sorted.values)

plt.xlabel("Ocorrências (menções)")
plt.title(f"{RQ} — Técnicas de XAI (ocorrências)")

max_val = counts_sorted.max()
x_pad = max(1, int(max_val * 0.02))

for bar in bars:
    w = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    plt.text(w + x_pad, y, f"{int(w)}", va="center")

plt.xlim(0, max_val + 6 * x_pad)
plt.tight_layout()
plt.subplots_adjust(left=0.55)

out_path1 = OUT_DIR / f"{RQ}_barras.png"
plt.savefig(out_path1, dpi=300)
plt.show()
print(f"Salvo em: {out_path1}")

#Gráfico 2: Heatmap de coocorrência
df_clean = pd.read_csv(DATA_DIR / "respostas_clean.csv")

rq8 = df_clean[["Título", "RQ8"]].copy()
rq8["RQ8"] = rq8["RQ8"].fillna("").astype(str)
rq8["RQ8"] = rq8["RQ8"].apply(lambda s: [x.strip() for x in s.split("+") if x.strip()])
rq8 = rq8.explode("RQ8").rename(columns={"RQ8": "Categoria"})
rq8 = rq8.dropna(subset=["Categoria"])

# aplica o mesmo agrupamento raro -> "Outros"
keep = set(main.index)
rq8["Categoria"] = rq8["Categoria"].apply(lambda x: x if x in keep else "Outros")

rq8 = rq8.drop_duplicates(["Título", "Categoria"])

mat = pd.crosstab(rq8["Título"], rq8["Categoria"])
co = mat.T.dot(mat)

plt.figure(figsize=(10, 8))
plt.imshow(co.values, aspect="auto")
plt.xticks(range(len(co.columns)), co.columns, rotation=45, ha="right")
plt.yticks(range(len(co.index)), co.index)
plt.title(f"{RQ} — Coocorrência de técnicas de XAI (por paper)")
plt.colorbar(label="Nº de papers com ambas as técnicas")
plt.tight_layout()

out_path2 = OUT_DIR / f"{RQ}_heatmap.png"
plt.savefig(out_path2, dpi=300)
plt.show()
print(f"Salvo em: {out_path2}")

#Gráfico 3: Pizza de quantidade de categorias por paper
unique_pairs = sub.drop_duplicates(["Título", "Categoria"])
k = unique_pairs.groupby("Título")["Categoria"].nunique()
dist = k.value_counts().sort_index()

labels = [str(i) for i in dist.index] 
values = dist.values

plt.figure(figsize=(9, 9))
plt.pie(
    values,
    labels=labels,
    autopct=lambda p: f"{p:.1f}%",
    startangle=90,
    textprops={"fontsize": 10},
)

plt.title(f"{RQ} — Quantidade de técnicas XAI por paper")
plt.tight_layout()

out_path3 = OUT_DIR / f"{RQ}_qtd_categorias_por_paper.png"
plt.savefig(out_path3, dpi=300)
plt.show()
print(f"Salvo em: {out_path3}")