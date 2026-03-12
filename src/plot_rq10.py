import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = Path("img/RQ10")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RQ = "RQ10"

df = pd.read_csv(DATA_DIR / "respostas_long.csv")
sub = df[df["RQ"] == RQ].copy()

MIN_COUNT = 3

counts = sub["Categoria"].value_counts()

main = counts[counts >= MIN_COUNT]
others = counts[counts < MIN_COUNT].sum()

counts_grouped = main.copy()
if others > 0:
    counts_grouped.loc["Outros"] = others

counts_sorted = counts_grouped.sort_values()

#Gráfico 1: Barras horizontais
plt.figure(figsize=(10,6))
bars = plt.barh(counts_sorted.index, counts_sorted.values)

plt.xlabel("Ocorrências")
plt.title(f"{RQ} — Tipos de métricas utilizadas")

max_val = counts_sorted.max()
x_pad = max(1, int(max_val * 0.02))

for bar in bars:
    w = bar.get_width()
    y = bar.get_y() + bar.get_height()/2
    plt.text(w + x_pad, y, f"{int(w)}", va="center")

plt.xlim(0, max_val + 6*x_pad)
plt.tight_layout()
plt.subplots_adjust(left=0.45)

out_path1 = OUT_DIR / f"{RQ}_barras.png"
plt.savefig(out_path1, dpi=300)
plt.show()

print(f"Salvo em: {out_path1}")


#Gráfico 2: Quantidade de métricas por paper
unique_pairs = sub.drop_duplicates(["Título","Categoria"])
k = unique_pairs.groupby("Título")["Categoria"].nunique()

dist = k.value_counts().sort_index()

labels = [str(i) for i in dist.index]
values = dist.values

plt.figure(figsize=(9,9))

plt.pie(
    values,
    labels=labels,
    autopct=lambda p: f"{p:.1f}%",
    startangle=90,
    textprops={"fontsize":10}
)

plt.title(f"{RQ} — Quantidade de métricas por paper")
plt.tight_layout()

out_path3 = OUT_DIR / f"{RQ}_qtd_metricas_por_paper.png"
plt.savefig(out_path3, dpi=300)
plt.show()

print(f"Salvo em: {out_path3}")