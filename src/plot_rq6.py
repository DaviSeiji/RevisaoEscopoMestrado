import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = Path("img/RQ6")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RQ = "RQ6"
df = pd.read_csv(DATA_DIR / "respostas_long.csv")
sub = df[df["RQ"] == RQ].copy()

order = ["Edge", "Cloud","Federated/Distribuído", "Não mencionado"]
counts = sub["Categoria"].value_counts().reindex(order).fillna(0).astype(int)

#Gráfico 1: Barras horizontais
counts_sorted = counts.sort_values()

plt.figure(figsize=(10, 6))
bars = plt.barh(counts_sorted.index, counts_sorted.values)

plt.xlabel("Nº de papers")
plt.title(f"{RQ} — Local de processamento (arquitetura)")

max_val = counts_sorted.max() if counts_sorted.max() > 0 else 1
x_pad = max(1, int(max_val * 0.03))

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

#Gráfico 2: Pizza
pct = (counts / counts.sum() * 100).round(1)

plt.figure(figsize=(9, 9))
plt.pie(
    pct.values,
    labels=pct.index,
    autopct=lambda p: f"{p:.1f}%",
    startangle=90,
    textprops={"fontsize": 11},
)
plt.title(f"{RQ} — Local de processamento (% de papers)")
plt.tight_layout()

out_path2 = OUT_DIR / f"{RQ}_pizza.png"
plt.savefig(out_path2, dpi=300)
plt.show()
print(f"Salvo em: {out_path2}")