# -*- coding: utf-8 -*-
# Little tool to convert Markdown to cool LaTeX documents.
# Written by YoPox on 09/18/2016

import re

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

inputFile = open('Arbres.md', 'r')
output = open('output.tex', 'w')

struct = []
par = []

for line in inputFile:
    level, text = parse(line)
    if level > 0:
        struct.append([level, text])
        par.append([])
    else:
        par[-1].append(line)

print(struct)
