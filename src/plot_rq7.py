import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = Path("img/RQ7")
OUT_DIR.mkdir(exist_ok=True)

RQ = "RQ7"

df = pd.read_csv(DATA_DIR / "respostas_long.csv")

sub = df[df["RQ"] == RQ].copy()

merge_map = {
    "GNN (Graph NN)": "Outros (GNN+RL+Neuro-simbólico)",
    "Reinforcement Learning (DRL/RL)": "Outros (GNN+RL+Neuro-simbólico)",
    "Neuro-simbólico / Regras (LTN, etc.)": "Outros (GNN+RL+Neuro-simbólico)",
}

sub["Categoria"] = sub["Categoria"].replace(merge_map)

# Gráfico 1: Ocorrências por algoritmo
counts = sub["Categoria"].value_counts().sort_values()  # opcional: menor->maior p/ ficar bonito

plt.figure(figsize=(10, 6))
bars = plt.barh(counts.index, counts.values)

plt.xlabel("Ocorrências em papers")
plt.title(f"{RQ} — Algoritmos de Deep Learning mais utilizados")

max_val = counts.max()
x_pad = max(1, int(max_val * 0.02))

for bar in bars:
    w = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    plt.text(w + x_pad, y, f"{int(w)}", va="center")

plt.xlim(0, max_val + 6 * x_pad)
plt.tight_layout()

out_path1 = OUT_DIR / f"{RQ}_ocorrencias.png"
plt.savefig(out_path1, dpi=300)
plt.show()
print(f"Salvo em: {out_path1}")


# Gráfico 2: Porcentagem de papers que mencionam cada categoria
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
plt.title(f"{RQ} — Presença por paper")

max_val = pct.max()
x_pad = max(0.5, max_val * 0.02)

for bar in bars:
    w = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    plt.text(w + x_pad, y, f"{w:.1f}%", va="center")

plt.xlim(0, min(100, max_val + 5 * x_pad))
plt.tight_layout()

out_path2 = OUT_DIR / f"{RQ}_porcentagem_paper.png"
plt.savefig(out_path2, dpi=300)
plt.show()
print(f"Salvo em: {out_path2}")

# Gráfico 3: Quantidade de categorias por paper
unique_pairs = sub.drop_duplicates(["Título", "Categoria"])
k = unique_pairs.groupby("Título")["Categoria"].nunique()
dist = k.value_counts().sort_index()  # ex: 1->quantos papers, 2->quantos papers...

labels = [str(i) for i in dist.index]  # "1", "2", "3", ...
values = dist.values

plt.figure(figsize=(9, 9))
plt.pie(
    values,
    labels=labels,
    autopct=lambda p: f"{p:.1f}%",
    startangle=90,
    textprops={"fontsize": 10},
)

plt.title(f"{RQ} — Quantidade de algoritmos por paper")
plt.tight_layout()

out_path3 = OUT_DIR / f"{RQ}_qtd_categorias_por_paper.png"
plt.savefig(out_path3, dpi=300)
plt.show()
print(f"Salvo em: {out_path3}")