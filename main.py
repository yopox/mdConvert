# -*- coding: utf-8 -*-
# Little tool to convert Markdown to cool LaTeX documents.
# Written by YoPox on 09/18/2016

## IMPORT
import re,sys

itemdeep = 0

def parse(chaine):
    chaine = re.sub(r"[*]{2}(?P<g>(.*))[*]{2}", r"\\textbf{\g<g>}", chaine)
    chaine = re.sub(r"_(?P<g>(.*))_", r"\\textit{\g<g>}", chaine)
    chaine = re.sub(r"[ ]*<br>", r" \\newline", chaine)
    chaine = re.sub(r"\* \* \*", r"", chaine)
    chaine = re.sub(r"^[#]{6} (?P<g>(.*))", r"\\subparagraph{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{5} (?P<g>(.*))", r"\\paragraph{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{4} (?P<g>(.*))", r"\\subsubsection{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{3} (?P<g>(.*))", r"\\subsection{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{2} (?P<g>(.*))", r"\\section{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{1} (?P<g>(.*))", r"\\chapter{\g<g>}", chaine)
    chaine = re.sub(r"[`]{3}[O|o](?P<g>(.*))", r"\\lstset{language=\g<g>}\n\\begin{lstlisting}", chaine)
    chaine = re.sub(r"[`]{3}raw", r"\\begin{lstlisting}", chaine)
    chaine = re.sub(r"^[`]{3}(?P<g>(.{1,}))", r"\\lstset{language=\g<g>}\n\\begin{lstlisting}", chaine)
    chaine = re.sub(r"^[`]{3}", r"\\end{lstlisting}", chaine)

    global itemdeep

    if re.match(r"^-[ ]*(?P<g>(.*))", chaine):
        if itemdeep == 0:
            itemdeep = 1
            chaine = re.sub(r"^-[ ]*(?P<g>(.*))", r"\\begin{itemize}\n\\item \g<g>", chaine)
        elif itemdeep > 1:
            chaine = re.sub(r"^-[ ]*(?P<g>(.*))", r"\\end{itemize}\n\\item \g<g>", chaine)
            itemdeep = 1
        else:
            chaine = re.sub(r"^-[ ]*(?P<g>(.*))", r"\\item \g<g>", chaine)

    elif re.match(r"^( {4})-[ ]*(?P<g>(.*))", chaine):
        if itemdeep == 1:
            chaine = re.sub(r"^( {4})-[ ]*(?P<g>(.*))", r"\\begin{itemize}\n\\item \g<g>", chaine)
            itemdeep = 2
        else:
            chaine = re.sub(r"^( {4})-[ ]*(?P<g>(.*))", r"\\item \g<g>", chaine)

    elif re.match(r"^[a-zA-Z]*", chaine) and itemdeep > 0 and chaine != "\n":
        while itemdeep > 0:
            chaine = "\end{itemize}" + chaine
            itemdeep -= 1

    # elif re.match(r"^-[ ]*(?P<g>(.*))", chaine):
    # chaine = re.sub(r"^[0-9]*\.[ ]*(?P<g>(.*))", r"\\item \g<g>", chaine)
    # chaine = re.sub(r"^( {4})[0-9]*\.[ ]*(?P<g>(.*))", r"\\item \g<g>", chaine)
    return chaine

s1 =  r"""\documentclass{report}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[frenchb]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{listings}
\usepackage{enumerate}
\usepackage{mathrsfs}"""

s2 = r"""\begin{document}
\nocite{*}

\maketitle
\tableofcontents"""

def tabler(textIn) :
    pass

## EXECUTION
if __name__ == '__main__' :

    # Sortie
    if len(sys.argv) == 2:            # If no output specified
        outFile = 'output.tex'        # output.tex' default
    elif len(sys.argv) > 2:           # If an output is specified
        outFile = sys.argv[2]         # It is used

    #Fonctionnement général
    if len(sys.argv) > 1 :            # Entry must be specified
        inFile = sys.argv[1]          # as first argument
        inputFile = open(inFile, 'r')
        output = open(outFile, 'w')

        output.seek(0)
        output.write(s1)
        output.write("\n\n")
        output.write(r"\title{" + input("Title : ") + "}")
        output.write("\n")
        output.write(r"\author{" + input("Author : ") + "}")
        output.write("\n\n")
        output.write(s2)
        output.write("\n")

        chaine = r""

        for line in inputFile:
            chaine += parse(line)

        output.write(chaine)

        output.write("\n")
        output.write(r"\end{document}")

        inputFile.close()
        output.close()

    else :                          # If no entry specified
        print('Usage : main.py input output')
