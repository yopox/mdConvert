# -*- coding: utf-8 -*-
# Little tool to convert Markdown to cool LaTeX documents.
# Written by YoPox on 09/18/2016

## IMPORT
import re,sys

itemdeep = 0
quote = False

def parse(chaine):
    # Bold
    chaine = re.sub(r"[*]{2}(?P<g>(.[^\*]*))[*]{2}", r"\\textbf{\g<g>}", chaine)
    # Italic
    if not "$" in chaine: # LaTeX uses _ for indices…
        chaine = re.sub(r"_(?P<g>(.[^_]*))_", r"\\textit{\g<g>}", chaine)
    # Strikethrough
    chaine = re.sub(r"[~]{2}(?P<g>(.[^~]*))[~]{2}", r"(\g<g>)", chaine)
    # New line in a paragraph
    chaine = re.sub(r"[ ]*<br>", r" \\newline", chaine)
    # Remove decoration
    chaine = re.sub(r"\* \* \*", r"", chaine)
    # Subsections
    chaine = re.sub(r"^[#]{6} (?P<g>(.*))", r"\\subparagraph{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{5} (?P<g>(.*))", r"\\paragraph{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{4} (?P<g>(.*))", r"\\subsubsection{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{3} (?P<g>(.*))", r"\\subsection{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{2} (?P<g>(.*))", r"\\section{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{1} (?P<g>(.*))", r"\\chapter{\g<g>}", chaine)
    # Ocaml specific code block
    chaine = re.sub(r"[`]{3}[O|o](?P<g>(.*))", r"\\lstset{language=\g<g>}\n\\begin{lstlisting}", chaine)
    # Raw code block (no color)
    chaine = re.sub(r"[`]{3}raw", r"\\begin{lstlisting}", chaine)
    # Generic code block
    chaine = re.sub(r"^[`]{3}(?P<g>(.{1,}))", r"\\lstset{language=\g<g>}\n\\begin{lstlisting}", chaine)
    # Code block end
    chaine = re.sub(r"^[`]{3}", r"\\end{lstlisting}", chaine)

    # Quotes
    global quote

    if re.match(r"^>[ ]*(?P<g>.*)", chaine):
        if quote == False:
            quote = True
            chaine = re.sub(r"^>[ ]*(?P<g>.*)", r"\n\\medskip\n\\begin{displayquote}\n\n\g<g>", chaine)
        else:
            chaine = re.sub(r"^>[ ]*(?P<g>.*)", r"\g<g>", chaine)
    elif quote == True:
        quote = False
        chaine = "\n\n\\end{displayquote}\n\\medskip\n" + chaine

    # Itemize
    global itemdeep

    # Main items
    if re.match(r"^-[ ]*(?P<g>(.*))", chaine):
        if itemdeep == 0:
            itemdeep = 1
            chaine = re.sub(r"^-[ ]*(?P<g>(.*))", r"\n\\medskip\n\\begin{itemize}\n\n\\item \g<g>", chaine)
        elif itemdeep > 1:
            chaine = re.sub(r"^-[ ]*(?P<g>(.*))", r"\n\n\\end{itemize}\n\n\\item \g<g>", chaine)
            itemdeep = 1
        else:
            chaine = re.sub(r"^-[ ]*(?P<g>(.*))", r"\\item \g<g>", chaine)
    # Subitems
    elif re.match(r"^( {4})-[ ]*(?P<g>(.*))", chaine):
        if itemdeep == 1:
            chaine = re.sub(r"^( {4})-[ ]*(?P<g>(.*))", r"\n\n\\begin{itemize}\n\n\\item \g<g>", chaine)
            itemdeep = 2
        else:
            chaine = re.sub(r"^( {4})-[ ]*(?P<g>(.*))", r"\\item \g<g>", chaine)
    # End list environment
    elif re.match(r"^[a-zA-Z]*", chaine) and itemdeep > 0 and chaine != "\n":
        while itemdeep > 0:
            chaine = "\n\n\\end{itemize}\n\n" + chaine
            itemdeep -= 1

    # TODO: Numeral lists
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
\usepackage{soul}
\usepackage{csquotes}
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
        parse1 = []

        for line in inputFile:
            chaine += parse(line)

        # Format line breaks
        chaine = re.sub(r"[\n]{2,}", r"\n\n", chaine)

        output.write(chaine)

        output.write("\n")
        output.write(r"\end{document}")

        inputFile.close()
        output.close()

    # If no entry specified
    else :
        print('Usage : main.py input output')
