import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = Path("img/RQ2")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RQ = "RQ2"

df_long = pd.read_csv(DATA_DIR / "respostas_long.csv")
sub = df_long[df_long["RQ"] == RQ].copy()

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
plt.title(f"{RQ} — Categorias (ocorrências)")

max_val = counts_sorted.max()
x_pad = max(1, int(max_val * 0.02))

for bar in bars:
    w = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    plt.text(w + x_pad, y, f"{int(w)}", va="center")

plt.xlim(0, max_val + 6 * x_pad)
plt.tight_layout()
plt.subplots_adjust(left=0.42)

out_path1 = OUT_DIR / f"{RQ}_barras.png"
plt.savefig(out_path1, dpi=300)
plt.show()
print(f"Salvo em: {out_path1}")

#Gráfico 2: Heatmap de coocorrência
df_clean = pd.read_csv(DATA_DIR / "respostas_clean.csv")

rq2 = df_clean[["Título", "RQ2"]].copy()
rq2["RQ2"] = rq2["RQ2"].fillna("").astype(str)
rq2["RQ2"] = rq2["RQ2"].apply(lambda s: [x.strip() for x in s.split("+") if x.strip()])
rq2 = rq2.explode("RQ2").rename(columns={"RQ2": "Categoria"})
rq2 = rq2.dropna(subset=["Categoria"])

keep = set(main.index)  
rq2["Categoria"] = rq2["Categoria"].apply(lambda x: x if x in keep else "Outros")

rq2 = rq2.drop_duplicates(["Título", "Categoria"])
mat = pd.crosstab(rq2["Título"], rq2["Categoria"])
co = mat.T.dot(mat)

plt.figure(figsize=(10, 8))
plt.imshow(co.values, aspect="auto")
plt.xticks(range(len(co.columns)), co.columns, rotation=45, ha="right")
plt.yticks(range(len(co.index)), co.index)
plt.title(f"{RQ} — Coocorrência de categorias (por paper)")
plt.colorbar(label="Nº de papers com ambas as categorias")
plt.tight_layout()

out_path2 = OUT_DIR / f"{RQ}_heatmap.png"
plt.savefig(out_path2, dpi=300)
plt.show()
print(f"Salvo em: {out_path2}")