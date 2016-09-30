# -*- coding: utf-8 -*-
# Little tool to convert Markdown to cool LaTeX documents.
# Written by YoPox and Hadrien

# IMPORT
import re
import sys

global quote, ARGV, itemdeep

quote = False
ARGV = {
    'output': "output.tex",
    'input': '',
    'author': '',
    'title': ''
}
itemdeep = 0


def argTraitement():
    global ARGV

    # input
    if len(sys.argv) > 1:
        ARGV['input'] = sys.argv[1]

    # liste des options possibles
    options = {
        '-o': 'output',
        '--ouput': 'output',
        '-d': 'date',
        '--date': 'date',
        '-a': 'author',
        '--author': 'author',
        '-t': 'title',
        '--title': 'title'
    }

    # traitement des options
    for i in range(2, len(sys.argv)):
        if sys.argv[i] in options and i + 1 < len(sys.argv):
            ARGV[options[sys.argv[i]]] = sys.argv[i + 1]


def parse(chaine):
    # déclaration des variables globales
    global itemdeep, quote

    # Bold
    chaine = re.sub(r"[*]{2}(?P<g>(.[^\*]*))[*]{2}", r"\\textbf{\g<g>}", chaine)
    # Italic
    if not "$" in chaine:  # LaTeX uses _ for indices…
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

    if re.match(r"^>[ ]*(?P<g>.*)", chaine):
        if quote == False:
            quote = True
            chaine = re.sub(r"^>[ ]*(?P<g>.*)", r"\n\\medskip\n\\begin{displayquote}\n\n\g<g>", chaine)
        else:
            chaine = re.sub(r"^>[ ]*(?P<g>.*)", r"\g<g>", chaine)
    elif quote == True:
        quote = False
        chaine = "\n\n\\end{displayquote}\n\\medskip\n" + chaine

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

def replTable(m):
    # m : match trouvé pour un tableau :
    # m.group(1) : tableau en entier
    # m.group(2) : 1ère ligne
    # m.group(6) : reste du tableau

    firstLine = [ col for col in m.group(2).split("|") if col != ""]
    nbCol = len(firstLine)
    result = "\\begin{tabular}{|" + "c|" * nbCol + "}\n\\hline\n"

    # Première colonne
    result += firstLine [0]
    for cell in firstLine[1:]:
        result += " & " + cell
    result += "\\\\\n "

    # Reste
    for line in m.group(6).split('\n'):
        tablLine = [ cell for cell in line.split("|") if cell != ""]
        if tablLine :
            result += "\\hline\n" + tablLine[0]
            for i,cell in enumerate(tablLine[1:]):
                if i < nbCol -1 :
                    result += " & " + cell
            result += "\\\\\n"

    return result + "\\hline \n\\end{tabular}\n"

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
\usepackage{mathrsfs}

"""

s2 = r"""

\begin{document}
\nocite{*}

\maketitle
\tableofcontents"""

# EXECUTION
if __name__ == '__main__':

    # Reading the arguments
    argTraitement()
    inFile = ARGV['input']
    outFile = ARGV['output']

    # Fonctionnement général
    if len(inFile) > 0:
        inputFile = open(inFile, 'r')
        output = open(outFile, 'w')

        output.seek(0)
        output.write(s1)
        output.write(r"\title{" + ARGV['title'] + "}")
        output.write("\n")
        output.write(r"\author{" + ARGV['author'] + "}")
        output.write("\n")
        if 'date' in ARGV:
            output.write(r"\date{" + ARGV['date'] + "}")
            output.write("\n")
        output.write(s2)
        output.write("\n")

        chaine = r""
        parse1 = []

        for line in inputFile:
            chaine += parse(line)

        # Format line breaks
        chaine = re.sub(r"[\n]{2,}", r"\n\n", chaine)

        # Format tables
        chaine = re.sub(
            r"(((\|[^\n|]+)*)(\s)*\|?(\s)*\| ?[\*-]{3,} ?\|[ \t]*\n[ \t]*((((\|([^|\n]*))+)\|?[ \t]*\n?)+))", replTable, chaine)
        output.write(chaine)

        output.write("\n")
        output.write(r"\end{document}")

        inputFile.close()
        output.close()

    # If no entry specified
    else:
        print(
            '''Usage : main.py input [-o/--output output.tex] [-a/--author "M. Me"] [-d/--date today] [-t/--title "My super title"]''')
