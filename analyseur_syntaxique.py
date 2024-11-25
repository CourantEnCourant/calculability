#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 18:22:48 2024

@author: guilhem
"""

#__________MODULES
import glob
import chardet
import networkx as nx
import matplotlib.pyplot as plt
import json

#__________FUNCTIONS

# Détection de l'encodage
def get_encoding (path: str) -> str:
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

def tokenize(path: str, file_encoding:str) -> list[str]:
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
            print(line)
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

def get_nodes_edges (code:list[str]) -> tuple[str, str]:
    """
    Analyse une liste de commandes pour extraire les nœuds et les arcs d'un graphe.

    Parameters:
    code (list): Une liste de chaînes représentant des commandes, où chaque commande peut être 
                 une instruction, une boucle ("boucle"), une condition ("si") ou une fermeture 
                 de bloc ("}").

    Return:
    tuple: Un tuple contenant deux éléments :
        - nodes (dict): Un dictionnaire associant chaque index de commande à la commande elle-même.
        - edges (list): Une liste de tuples représentant les arcs entre les nœuds, où chaque 
                        tuple est de la forme (nœud_source, nœud_cible).
    """
    
    open_bracket = list()
    loops = list()
    nodes = dict()
    
    for i, command in enumerate(code):
        if command == "boucle" or command == "si":
            open_bracket.append(i)
        elif command == "}":
            matching = (open_bracket[-1], i)
            loops.append(matching)
            open_bracket = open_bracket[:-1]
        
        # Associer des noms aux nœuds
        nodes[i] = command
        # print(i, command)
    
    # Ajouter des arcs
    edges = list()
    lenght_graph = len(nodes)
    for r in range(lenght_graph - 1):
        edge = (r, r+1)
        edges.append(edge)
    
    # Ajouter des loops
    for loop in loops:
        edge = (loop[1], loop[0])
        edges.append(edge)

    return nodes, edges

def save_json(nodes:dict, edges:list, json_file:str) -> None:
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

#__________MAIN

path = "../turing_java/programmesTS/01.1.TS"

file_encoding = get_encoding(path)

tokens = tokenize(path, file_encoding)

nodes, edges = get_nodes_edges(tokens)

json_file = "data.json"
save_json(nodes, edges, json_file)
        
# Créer un graphe orienté
G = nx.DiGraph()

for arrow in edges:
    G.add_edge(arrow[0], arrow[1])

# Dessiner le graphe avec les étiquettes personnalisées
pos = nx.kamada_kawai_layout(G)
plt.figure(figsize=(12, 8))  # Ajuste les dimensions
nx.draw(G, pos, with_labels=False, node_color="lightblue", arrows=True)
nx.draw_networkx_labels(G, pos, nodes)

