import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = Path("img/RQ11")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RQ = "RQ11"

df_long = pd.read_csv(DATA_DIR / "respostas_long.csv")
sub = df_long[df_long["RQ"] == RQ].copy()

counts = sub["Categoria"].value_counts()

MIN_COUNT = 4
main = counts[counts >= MIN_COUNT]
others = counts[counts < MIN_COUNT].sum()

counts_grouped = main.copy()
if others > 0:
    counts_grouped.loc["Outros"] = others

#Gráfico 1: Barras horizontais
counts_sorted = counts_grouped.sort_values()

plt.figure(figsize=(10, 6))
bars = plt.barh(counts_sorted.index, counts_sorted.values)

plt.xlabel("Ocorrências (menções)")
plt.title(f"{RQ} — Desafios e lacunas reportados")

max_val = counts_sorted.max()
x_pad = max(1, int(max_val * 0.02))

for bar in bars:
    w = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    plt.text(w + x_pad, y, f"{int(w)}", va="center")

plt.xlim(0, max_val + 6 * x_pad)
plt.tight_layout()
plt.subplots_adjust(left=0.48)

out_path1 = OUT_DIR / f"{RQ}_barras.png"
plt.savefig(out_path1, dpi=300)
plt.show()
print(f"Salvo em: {out_path1}")

#Gráfico 2: Porcentagem de papers que mencionam cada categoria

n_papers = sub["Título"].nunique()

papers_per_cat = (
    sub.drop_duplicates(["Título", "Categoria"])
       .groupby("Categoria")["Título"]
       .nunique()
       .sort_values(ascending=False)
)

pct = (papers_per_cat / n_papers * 100).round(1).sort_values()

plt.figure(figsize=(10, 6))
bars = plt.barh(pct.index, pct.values)

plt.xlabel("% de papers que mencionam")
plt.title(f"{RQ} — Presença de desafios na literatura")

max_val = pct.max()
x_pad = max(0.5, max_val * 0.02)

for bar in bars:
    w = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    plt.text(w + x_pad, y, f"{w:.1f}%", va="center")

plt.xlim(0, min(100, max_val + 5 * x_pad))
plt.tight_layout()
plt.subplots_adjust(left=0.45)

out_path2 = OUT_DIR / f"{RQ}_porcentagem_paper.png"
plt.savefig(out_path2, dpi=300)
plt.show()

print(f"Salvo em: {out_path2}")

#Gráfico 3: Quantidade de categorias por paper
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

plt.title(f"{RQ} — Quantidade de desafios/lacunas por paper")
plt.tight_layout()

out_path3 = OUT_DIR / f"{RQ}_qtd_categorias_por_paper.png"
plt.savefig(out_path3, dpi=300)
plt.show()
print(f"Salvo em: {out_path3}")