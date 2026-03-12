import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = Path("img/RQ1")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RQ = "RQ1"
df = pd.read_csv(DATA_DIR / "respostas_long.csv")
sub = df[df["RQ"] == RQ].copy()

counts = sub["Categoria"].value_counts()

#Categorias com poucas ocorrências serão agrupadas em "Outros"
MIN_COUNT = 3 
main = counts[counts >= MIN_COUNT]
others = counts[counts < MIN_COUNT].sum()

counts_grouped = main.copy()
if others > 0:
    counts_grouped.loc["Outros"] = others

#Gráfico 1: Contagem de ocorrências por categoria
counts_sorted = counts_grouped.sort_values()

plt.figure(figsize=(10, 6))
bars = plt.barh(counts_sorted.index, counts_sorted.values)

plt.xlabel("Nº de papers")
plt.title(f"{RQ} — Setor (contagem)")

max_val = counts_sorted.max()
x_pad = max(1, int(max_val * 0.02))

for bar in bars:
    w = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    plt.text(w + x_pad, y, f"{int(w)}", va="center")

plt.xlim(0, max_val + 6 * x_pad)
plt.tight_layout()
plt.subplots_adjust(left=0.35)

out_path1 = OUT_DIR / f"{RQ}_barras.png"
plt.savefig(out_path1, dpi=300)
plt.show()
print(f"Salvo em: {out_path1}")


#Gráfico 2: Porcentagem de papers por categoria
pct = (counts_grouped / counts_grouped.sum() * 100).round(1)

plt.figure(figsize=(9, 9))
plt.pie(
    pct.values,
    labels=pct.index,
    autopct=lambda p: f"{p:.1f}%",
    startangle=90,
    textprops={"fontsize": 10},
)
plt.title(f"{RQ} — Setor (% de ocorrências)")
plt.tight_layout()

out_path2 = OUT_DIR / f"{RQ}_pizza.png"
plt.savefig(out_path2, dpi=300)
plt.show()
print(f"Salvo em: {out_path2}")
