import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = Path("img/RQ9")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RQ = "RQ9"

df = pd.read_csv(DATA_DIR / "respostas_long.csv")
sub = df[df["RQ"] == RQ].copy()

counts = sub["Categoria"].value_counts()

pct = (counts / counts.sum() * 100).round(1)

plt.figure(figsize=(8,8))

plt.pie(
    pct.values,
    labels=pct.index,
    autopct=lambda p: f"{p:.1f}%",
    startangle=90,
    textprops={"fontsize":11}
)

plt.title(f"{RQ} — Escopo das explicações XAI")
plt.tight_layout()

out_path = OUT_DIR / f"{RQ}_pizza.png"
plt.savefig(out_path, dpi=300)
plt.show()

print(f"Salvo em: {out_path}")