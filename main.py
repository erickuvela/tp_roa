import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt


class Graphe:
    def __init__(self):
        self.graph = {}

    def ajouter_sommet(self, nom):
        if nom not in self.graph:
            self.graph[nom] = []

    def ajouter_arete(self, u, v):
        if u in self.graph and v in self.graph:
            self.graph[u].append(v)

    def tarjan(self):
        index = 0
        stack = []
        indices = {}
        low = {}
        onStack = set()
        result = []

        def dfs(node):
            nonlocal index
            indices[node] = index
            low[node] = index
            index += 1
            stack.append(node)
            onStack.add(node)

            for voisin in self.graph[node]:
                if voisin not in indices:
                    dfs(voisin)
                    low[node] = min(low[node], low[voisin])
                elif voisin in onStack:
                    low[node] = min(low[node], indices[voisin])

            if low[node] == indices[node]:
                comp = []
                while True:
                    w = stack.pop()
                    onStack.remove(w)
                    comp.append(w)
                    if w == node:
                        break
                result.append(comp)

        for sommet in self.graph:
            if sommet not in indices:
                dfs(sommet)

        return result

    def stats(self, cfc):
        total_aretes = sum(len(v) for v in self.graph.values())
        return {
            "sommets": len(self.graph),
            "aretes": total_aretes,
            "cfc": len(cfc)
        }

def sauvegarder_graphe(self, filename="graphe.png"):
    G = nx.DiGraph()

    for u in self.graph:
        G.add_node(u)
        for v in self.graph[u]:
            G.add_edge(u, v)

    plt.figure(figsize=(8,6))
    pos = nx.spring_layout(G)

    nx.draw(G, pos,
            with_labels=True,
            node_color='lightblue',
            node_size=2000,
            arrows=True)

    plt.title("Graphe sauvegardé")
    plt.savefig(filename)
    plt.close()

    print(f"Graphe enregistré sous {filename}")

    def dessiner(self):
        G = nx.DiGraph()
        for u in self.graph:
            G.add_node(u)
            for v in self.graph[u]:
                G.add_edge(u, v)

        plt.figure(figsize=(8,6))
        nx.draw(G, with_labels=True, node_color="lightblue", node_size=2000, arrows=True)
        plt.title("Visualisation du graphe")
        plt.show()



# =============================
# INTERFACE GRAPHIQUE
# =============================

g = Graphe()

def ajouter_commune():
    try:
        nom = entry_sommet.get().strip()

        if not nom:
            raise ValueError("Nom vide")

        if nom in g.graph:
            raise ValueError("Commune déjà existante")

        g.ajouter_sommet(nom)
        listbox.insert(tk.END, nom)
        entry_sommet.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def ajouter_relation():
    try:
        u = entry_depart.get().strip()
        v = entry_arrivee.get().strip()

        if u not in g.graph or v not in g.graph:
            raise ValueError("Commune non définie")

        g.ajouter_arete(u, v)
        relations.insert(tk.END, f"{u} → {v}")

        entry_depart.delete(0, tk.END)
        entry_arrivee.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def sauvegarder():
    try:
        g.sauvegarder_graphe()
        messagebox.showinfo("Succès", "Graphe enregistré !")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def lancer_tarjan():
    try:
        if not g.graph:
            raise ValueError("Aucune donnée")

        cfc = g.tarjan()

        output.delete(1.0, tk.END)
        output.insert(tk.END, "Résultats :\n\n")

        for comp in cfc:
            if len(comp) > 1:
                output.insert(tk.END, f"{comp} → Zone connectée\n")
            else:
                output.insert(tk.END, f"{comp} → Isolée\n")

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def dessiner():
    g.dessiner()



# =============================
# FENÊTRE
# =============================

root = tk.Tk()
root.title("Analyse des Communes - Tarjan")
root.geometry("700x600")

# Ajouter sommet
tk.Label(root, text="Nom de la commune").pack()
entry_sommet = tk.Entry(root)
entry_sommet.pack()
tk.Button(root, text="Ajouter Commune", command=ajouter_commune).pack()

listbox = tk.Listbox(root)
listbox.pack()

# Ajouter relation
tk.Label(root, text="Relation (Départ → Arrivée)").pack()
entry_depart = tk.Entry(root)
entry_depart.pack()
entry_arrivee = tk.Entry(root)
entry_arrivee.pack()

tk.Button(root, text="Ajouter Relation", command=ajouter_relation).pack()

relations = tk.Listbox(root)
relations.pack()

# Boutons
tk.Button(root, text="Lancer Tarjan", command=lancer_tarjan, bg="green").pack()
tk.Button(root, text="Afficher Graphe", command=dessiner, bg="blue").pack()

tk.Button(root, text="Sauvegarder Graphe", command=sauvegarder, bg="orange").pack()

# Résultats
output = tk.Text(root, height=10)
output.pack()

root.mainloop()
