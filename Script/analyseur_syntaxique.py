#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 18:22:48 2024

@author: guilhem
"""

# __________MODULES

import argparse
import logging
import chardet # requirement.txt
import networkx as nx # requirement.txt
import matplotlib.pyplot as plt # requirement.txt
import scipy as sp # requirement.txt
import json

# __________FUNCTIONS

def get_encoding(path: str) -> str:
    """
    Détecte l'encodage d'un fichier.

    Parametrers:
    path (str): Le chemin du fichier dont l'encodage doit être détecté.

    Return:
    str: L'encodage détecté du fichier (par exemple, 'utf-8', 'iso-8859-1', etc.).
    """

    with open(path, "rb") as fichier:
        contenu_binaire = fichier.read()
        detection = chardet.detect(contenu_binaire)
        encodage = detection['encoding']
        return encodage


def tokenize(path: str, file_encoding: str) -> list[str]:
    """
    Tokenise le contenu d'un fichier en extrayant les commandes.

    Parameters:
    path (str): Le chemin du fichier à lire.
    file_encoding (str): L'encodage du fichier (par exemple, 'utf-8').

    Return:
    list[str]: Une liste de chaînes représentant les commandes extraites du fichier.
    """

    with open(path, "r", encoding=file_encoding) as file:
        content = file.readlines()
        lines = list()
        for line in content:
            line = line.strip()
            # print(line)
            if line == "" or line.startswith("%"):
                pass
            else:
                lines.append(line)
        commands = list()
        for command in lines:
            command = command.split()
            for item in command:
                commands.append(item)
    return commands


def get_nodes_edges(tokens: list[str]) -> tuple[dict, list[tuple]]:
    """
    Traite une liste de tokens pour extraire les nœuds et les arêtes en vue de produire une représentation sous forme de graphe.
    
    Paramater:
        tokens (list[str]): Une liste de tokens représentant des éléments d'une structure de code.
    
    Returns:
        tuple[dict, list[tuple]]:
            - dict : Un dictionnaire associant les indices des nœuds à leurs étiquettes (tokens).
            - list[tuple] : Une liste des arêtes, chaque arête étant représentée par un tuple 
              d'indices de nœuds.
    """
    
    del_nodes = []
    open_loop = []
    node_n_label = {}
    edges = []
    loop = False
    
    for i, tok in enumerate(tokens):
        # print(i, tok, open_loop)
        node_n_label[i] = tok
        if tok == "boucle":
            loop = True
            open_loop.append(i)
        elif tok == "si":
            open_loop.append(i)
        elif open_loop and tokens[open_loop[-1]] == "si" and tok == "}":
            matching = (open_loop[-1], i)
            edges.append(matching)
            # print(matching)
            if loop:
                count = 0
                for r in range(i, len(tokens)):
                    if count == 0:
                        edges.pop()
                        matching = (open_loop[-1], r + 1)
                        edges.append(matching)
                        # print(">", tokens[r], matching)
                        count += 1
                        del_nodes.append(r + 1)
                    else:
                        matching = (r, r + 1)
                        edges.append(matching)
                        # print(">", tokens[r], matching)
                        del_nodes.append(r + 1)
                    if r + 1 < len(tokens) and tokens[r + 1] == "}":
                        break
                open_loop.pop()
        elif open_loop and tokens[open_loop[-1]] == "boucle" and tok == "}":
            matching = (i, open_loop[-1])
            edges.append(matching)
            # print(matching)
            open_loop.pop()
    
    nodes = [j for j in range(len(tokens)) if j not in del_nodes]
    
    for n in range(len(nodes)-1):
        matching = (nodes[n], nodes[n+1])
        edges.append(matching)
        
    return node_n_label, edges


def save_json(nodes: dict, edges: list[tuple], json_file: str) -> None:
    """
    Enregistre les nœuds et les arcs dans un fichier JSON.

    Parameters:
    nodes (dict): Un dictionnaire représentant les nœuds, où chaque clé est un identifiant de 
                  nœud et chaque valeur est la donnée associée à ce nœud.
    edges (list): Une liste de tuples représentant les arcs, où chaque tuple est de la forme 
                  (nœud_source, nœud_cible).
    json_file (str): Le chemin du fichier dans lequel les données doivent être enregistrées.

    Return:
    None: Cette fonction ne retourne rien. Elle effectue une opération d'écriture dans un fichier.
    """

    data = dict()
    data["nodes"] = nodes
    data["edges"] = edges

    # Écrire le dictionnaire data dans un fichier JSON
    with open(json_file, 'w') as fichier:
        json.dump(data, fichier, indent=4)


# __________MAIN

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Analyseur syntaxique python de la syntaxe des programmes MTddV.')
    parser.add_argument('-f', '--file_path', type=str, help='Chemin vers le fichier à parser.')
    parser.add_argument('-j', '--json', action="store_true", help='Enregistre les données parsé au format JSON.')
    parser.add_argument('-g', '--graph', action="store_true", help='Enregistre une représentation graphique des données parsé.')

    args = parser.parse_args()
    path = args.file_path
    # print(f"{path=}")
    # print(f"{args.json=}")
    # print(f"{args.graph=}")

    json_path = path.split("/")[-1]
    json_path = json_path.split(".")[0]
    json_path = "../Output/data_json/" + json_path + ".json"
    # print(json_path)
    
    graph_path = path.split("/")[-1]
    graph_path = graph_path.split(".")[0]
    graph_path = "../Output/graph/" + graph_path + ".png"
    # print(graph_path)
    
    # Configurer le niveau minimal de journalisation
    logging.basicConfig(level=logging.INFO)
    
    file_encoding = get_encoding(path)

    tokens = tokenize(path, file_encoding)

    nodes, edges = get_nodes_edges(tokens)
 
    # Créer un fichier json
    if args.json:
        save_json(nodes, edges, json_path)
        logging.info(f"Représentation JSON voir : {json_path}")
    else:
        logging.info(" Argument --json désactivé ")

    # Créer un graphe orienté
    if args.graph:
        G = nx.DiGraph()
        for arrow in edges:
            G.add_edge(arrow[0], arrow[1])
    
        # Dessiner le graphe avec les étiquettes personnalisées
        pos = nx.kamada_kawai_layout(G)
        plt.figure(figsize=(12, 8))  # Ajuste les dimensions
        nx.draw(G, pos, with_labels=False, node_color="lightblue", arrows=True)
        nx.draw_networkx_labels(G, pos, nodes)
        
        plt.savefig(graph_path)  # Vous pouvez changer l'extension pour d'autres formats
        plt.close()
        logging.info(f"Représentation graphique voir : {graph_path}")
    else:
        logging.info(" Argument --graph désactivé ")
    
    
    
    
    