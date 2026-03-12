import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = Path("img/RQ5")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RQ = "RQ5"

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
plt.title(f"{RQ} — Tipos de dados utilizados (ocorrências)")

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

rq5 = df_clean[["Título", "RQ5"]].copy()
rq5["RQ5"] = rq5["RQ5"].fillna("").astype(str)

rq5["RQ5"] = rq5["RQ5"].apply(lambda s: [x.strip() for x in s.split("+") if x.strip()])
rq5 = rq5.explode("RQ5").rename(columns={"RQ5": "Categoria"})
rq5 = rq5.dropna(subset=["Categoria"])

keep = set(main.index)
rq5["Categoria"] = rq5["Categoria"].apply(lambda x: x if x in keep else "Outros")

rq5 = rq5.drop_duplicates(["Título", "Categoria"])

mat = pd.crosstab(rq5["Título"], rq5["Categoria"])
co = mat.T.dot(mat)

plt.figure(figsize=(10, 8))
plt.imshow(co.values, aspect="auto")
plt.xticks(range(len(co.columns)), co.columns, rotation=45, ha="right")
plt.yticks(range(len(co.index)), co.index)
plt.title(f"{RQ} — Coocorrência de tipos de dados (por paper)")
plt.colorbar(label="Nº de papers com ambos os tipos")
plt.tight_layout()

out_path2 = OUT_DIR / f"{RQ}_heatmap.png"
plt.savefig(out_path2, dpi=300)
plt.show()
print(f"Salvo em: {out_path2}")