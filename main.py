# -*- coding: utf-8 -*-
# Little tool to convert Markdown to cool LaTeX documents.
# Written by YoPox on 09/18/2016

## IMPORT
import re,sys

## FUNCTIONS
# Removes the spaces at the beggining
def remSpaces(chaine):
    while chaine[0] == " ":
        chaine = chaine[1:]
    if "\n" in chaine:
        chaine = chaine[:-1]
    return chaine

# Return
def parse(chaine):
    nb = 0
    while chaine[0] == "#":
        nb = nb + 1
        chaine = chaine[1:]
    chaine = re.sub(r"[*]{2}(?P<g>(.*))[*]{2}", r"\textbf{\g<g>}", chaine)
    return nb, remSpaces(chaine)

## Paragraphs
def paragrapher(inputFile) :
    struct = []
    par = []

    for line in inputFile:
        level, text = parse(line)
        if level > 0:
            struct.append([level, text])
            par.append([])
        else:
            par[-1].append(line)

    return struct

def tabler(textIn) :
    return textIn

## EXECUTION
if __name__ == '__main__' :
    # Sortie
    if len(sys.argv) == 2:              # Si pas de sortie précisée
        outFile = '../output.tex'       # '../output.tex' par défaut
    elif len(sys.argv) > 2:             # Si une sortie est précisée
        outFile = sys.argv[2]           # on l'utilise

    #Fonctionnement général
    if len(sys.argv) > 1 :              # Un fichier d'entrée doit être précisé
        inFile = sys.argv[1]            # en premier argument
        inputFile = open(inFile, 'r')
        output = open(outFile, 'w')
        sys.stdout = output             # on utilise print pour écrire dans le fichier

        inText = inputFile.read()       # permet de faire des recherches sur le texte comme string
        for line in  :
            #paragrapher
            print(remSpaces(line))      # A modifier

    else :                              # Si pas de fichier d'entrée précisé
        print('No file to treat.')      # Real print, affiche qu'on ne peut rien faire
