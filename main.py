# -*- coding: utf-8 -*-
# Little tool to convert Markdown to cool LaTeX documents.
# Written by YoPox and Hadrien

# IMPORT
import re
import sys

global quote, ARGV, itemdeep

quote = False
code = False
nonBreakingBlock = False
ARGV = {
    'output': "output.tex",
    'input': '',
    'author': '',
    'title': '',
    'documentclass': 'report',
    'tableofcontents': False,
    'help': False,
}
itemdeep = 0


def argTraitement():
    global ARGV

    # input
    if len(sys.argv) > 1 and sys.argv[1][0] != '-':
        ARGV['input'] = sys.argv[1]

    # liste des options possibles
    options_args = {
        '-o': 'output',
        '--ouput': 'output',
        '-d': 'date',
        '--date': 'date',
        '-a': 'author',
        '--author': 'author',
        '-t': 'title',
        '--title': 'title',
        '-c': 'documentclass',
        '--documentclass': 'documentclass',
    }
    options_bools = {
        '-T': 'tableofcontents',
        '--tableofcontents': 'tableofcontents',
        '-h': 'help',
        '--help': 'help',
    }

    # traitement des options
    for i in range(1, len(sys.argv)):
        if sys.argv[i] in options_args and i + 1 < len(sys.argv):
            ARGV[options[sys.argv[i]]] = sys.argv[i + 1]
        if sys.argv[i] in options_bools:
            ARGV[options_bools[sys.argv[i]]] = True


def parse(chaine):
    # déclaration des variables globales
    global itemdeep, quote, code, nonBreakingBlock

    if code:
        chaine = re.sub(r"[é]", r"e", chaine)

    if "```" in chaine:
        code = not code

    # Horyzontal rule
    chaine = re.sub(r"^[-\*_]{3,}", "\\hrulefill\n", chaine)

    # Bold
    chaine = re.sub(r"[*]{2}(?P<g>(.[^\*]*))[*]{2}",
                    r"\\textbf{\g<g>}", chaine)
    # Italic
    # LaTeX uses _ for indices…
    if not "$" in chaine and not "\[" in chaine and not code:
        chaine = re.sub(r"[_](?P<g>(.[^_]*))[_]", r"\\textit{\g<g>}", chaine)
        # Strikethrough
        chaine = re.sub(r"[~]{2}(?P<g>(.[^~]*))[~]{2}", r"(\g<g>)", chaine)
    # New line in a paragraph
    chaine = re.sub(r"[ ]*<br>", r" \\newline", chaine)
    # Remove decoration
    chaine = re.sub(r"\* \* \*", r"", chaine)
    # Subsections
    if not code:
        chaine = re.sub(r"^[#]{6} (?P<g>(.*))", r"\\subparagraph{\g<g>}", chaine)
        chaine = re.sub(r"^[#]{5} (?P<g>(.*))", r"\\paragraph{\g<g>}", chaine)
        chaine = re.sub(r"^[#]{4} (?P<g>(.*))", r"\\subsubsection{\g<g>}", chaine)
        chaine = re.sub(r"^[#]{3} (?P<g>(.*))", r"\\subsection{\g<g>}", chaine)
        chaine = re.sub(r"^[#]{2} (?P<g>(.*))", r"\\section{\g<g>}", chaine)
        chaine = re.sub(r"^[#]{1} (?P<g>(.*))", r"\\chapter{\g<g>}", chaine)
    # Ocaml specific code block
    chaine = re.sub(r"[`]{3}[O|o](?P<g>(.*))",
                    r"\\lstset{language=\g<g>}\n\\begin{lstlisting}", chaine)
    # Raw code block (no color)
    chaine = re.sub(r"[`]{3}raw", r"\\begin{lstlisting}", chaine)
    # Non breaking raw code block (no color)
    if re.match(r"[`]{3}nbraw", chaine):
        chaine = re.sub(
            r"[`]{3}nbraw", r"\\begin{figure}[!htbp]\n\\centering\n\\begin{tabular}{c}\n\\begin{lstlisting}\n", chaine)
        nonBreakingBlock = True
    # Generic code block
    chaine = re.sub(r"^[`]{3}(?P<g>(.{1,}))",
                    r"\\lstset{language=\g<g>}\n\\begin{lstlisting}", chaine)
    # Code block end
    if re.match(r"^[`]{3}", chaine):
        if nonBreakingBlock:
            chaine = re.sub(r"^[`]{3}", r"\\end{lstlisting}\n\end{tabular}\n\\end{figure}\n", chaine)
            nonBreakingBlock = False
        else:
            chaine = re.sub(r"^[`]{3}", r"\\end{lstlisting}", chaine)

    # Comments
    chaine = re.sub(
        r"<!(\-{2}(?P<comment>[^-]*)\-{2})*> ?\n?", "% \g<comment>\n", chaine)

    # Links
    if "$" not in chaine:  # Latex math mode uses []()
        # link like "[This is google](http://www.google.com)"
        chaine = re.sub(r"""\[(?P<text>.*)\]\((?P<link>[^ ]*)( ".*")?\)""",
                        "\\href{\g<link>}{\g<text>}", chaine)
    # Links like "<http://www.google.com>"
    chaine = re.sub(
        r"\<(?P<link>https?://[^ ]*)\>", "\\href{\g<link>}{\g<link>}", chaine)
    # Links like " http://www.google.com "
    chaine = re.sub(
        r" (?P<link>https?://[^ ]*) ", " \\href{\g<link>}{\g<link>} ", chaine)

    # Quotes
    if not code:
        if re.match(r"^>[ ]*(?P<g>.*)", chaine):
            if quote == False:
                quote = True
                chaine = re.sub(
                    r"^>[ ]*(?P<g>.*)", r"\n\\medskip\n\\begin{displayquote}\n\n\g<g>", chaine)
            else:
                chaine = re.sub(r"^>[ ]*(?P<g>.*)", r"\g<g>", chaine)
        elif quote == True:
            quote = False
            chaine = "\n\n\\end{displayquote}\n\\medskip\n" + chaine

    # Main items
    if re.match(r"^-[ ]*(?P<g>(.*))", chaine):
        if itemdeep == 0:
            itemdeep = 1
            chaine = re.sub(
                r"^-[ ]*(?P<g>(.*))", r"\n\\medskip\n\\begin{itemize}\n\n\\item \g<g>", chaine)
        elif itemdeep > 1:
            chaine = re.sub(r"^-[ ]*(?P<g>(.*))",
                            r"\n\n\\end{itemize}\n\n\\item \g<g>", chaine)
            itemdeep = 1
        else:
            chaine = re.sub(r"^-[ ]*(?P<g>(.*))", r"\\item \g<g>", chaine)
    # Subitems
    elif re.match(r"^( {4})-[ ]*(?P<g>(.*))", chaine):
        if itemdeep == 1:
            chaine = re.sub(
                r"^( {4})-[ ]*(?P<g>(.*))", r"\n\n\\begin{itemize}\n\n\\item \g<g>", chaine)
            itemdeep = 2
        else:
            chaine = re.sub(r"^( {4})-[ ]*(?P<g>(.*))",
                            r"\\item \g<g>", chaine)
    # End list environment
    elif re.match(r"^[a-zA-Z]*", chaine) and itemdeep > 0 and chaine != "\n":
        while itemdeep > 0:
            chaine = "\n\n\\end{itemize}\n\\medskip\n" + chaine
            itemdeep -= 1

    # TODO: Numeral lists
    # elif re.match(r"^-[ ]*(?P<g>(.*))", chaine):
    # chaine = re.sub(r"^[0-9]*\.[ ]*(?P<g>(.*))", r"\\item \g<g>", chaine)
    # chaine = re.sub(r"^( {4})[0-9]*\.[ ]*(?P<g>(.*))", r"\\item \g<g>", chaine)

    return chaine


def replTable(m):
    # m : match trouvé pour un tableau :
    # m.group(0) : tableau en entier
    # m.group(1) : 1ère ligne
    # m.group(5) : ligne de centrage
    # m.group(7) : reste du tableau
    # pour plus de renseignements : n est a adapter
    # for i in range(n): print(i," : ",m.group(i))

    firstLine = [col for col in m.group(1).split("|") if col != ""]
    centerLine = [col for col in m.group(5).split("|") if col != ""]
    nbCol = len(firstLine)
    result = "\\begin{center}\n\\begin{tabular}{|"

    # Traitement du centrage
    def dispoCell(cell):
        liste = [char for char in cell if char != " "]
        if liste[0] == ":" and liste[-1] == ":":
            return 'c'
        if liste[-1] == ":":
            return 'r'
        return 'l'

    for i in range(nbCol):
        if i < len(centerLine):
            result += dispoCell(centerLine[i]) + "|"
        else:
            result += "l|"

    result += "}\n\\hline\n"

    # Première colonne
    result += firstLine[0]
    for cell in firstLine[1:]:
        result += " & " + cell
    result += "\\\\\n "

    # Reste
    for line in m.group(7).split('\n'):
        tablLine = [cell for cell in line.split("|") if cell != ""]
        if tablLine:
            result += "\\hline\n" + tablLine[0]
            for i, cell in enumerate(tablLine[1:]):
                if i < nbCol - 1:
                    result += " & " + cell
            result += "\\\\\n"

    return result + "\\hline \n\\end{tabular}\n\\end{center}\n"

s1 =  r"""\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[frenchb]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{listings}
\usepackage{enumerate}
\usepackage{soul}
\usepackage{csquotes}
\usepackage{mathrsfs}
\usepackage{hyperref} % liens
\usepackage[official]{eurosym} % pour le symbole euro

"""

s2 = r"""
\begin{document}
\nocite{*}

\maketitle"""

usage = """Usage : main.py input OPTIONS   : convert md to LaTeX
        main.py -h/--help       : show the help page"""


# EXECUTION
if __name__ == '__main__':

    # Reading the arguments
    argTraitement()

    if ARGV['help']:
        help_file = open("help.txt", 'r')
        for line in help_file:
            print(line, end='')
        help_file.close()

    # Fonctionnement général
    elif len(ARGV['input']) > 0:
        try:
            inputFile = open(ARGV['input'], 'r')
        except FileNotFoundError:
            print("Fichier non trouvé !")
            print(usage)
        else:  # Comportement normal
            output = open(ARGV['output'], 'w')

            print("Traitement de : ", ARGV['input'], "...")

            output.seek(0)
            output.write("\\documentclass{" + ARGV['documentclass'] + "}\n")
            output.write(s1)
            output.write(r"\title{" + ARGV['title'] + "}")
            output.write("\n")
            output.write(r"\author{" + ARGV['author'] + "}")
            output.write("\n")
            if 'date' in ARGV:
                output.write(r"\date{" + ARGV['date'] + "}")
                output.write("\n")
            output.write(s2)
            if ARGV['tableofcontents']:
                output.write("\n\\tableofcontents\n")
            output.write("\n")

            chaine = r""
            parse1 = []

            for line in inputFile:
                chaine += parse(line)

            # Convert euro symbole to LaTeX command
            chaine = re.sub(r"€", "\\euro{}", chaine)

            # Format line breaks
            chaine = re.sub(r"\\medskip", r"\n\\medskip\n", chaine)
            chaine = re.sub(r"[\n]{2,}", r"\n\n", chaine)
            chaine = re.sub(r"\\medskip[\n]{1,}\\medskip", r"\n\\medskip\n", chaine)

            # Format tables
            chaine = re.sub(
                r"((\|[^\n|]+)*)(\s)*\|?(\s)*((\| ?:?-+:? ?)+)\|[ \t]*\n[ \t]*((((\|([^|\n]*))*)\|?[ \t]*\n?)+)", replTable, chaine)
            output.write(chaine)

            output.write("\n")
            output.write(r"\end{document}")

            inputFile.close()
            output.close()

            print("LaTeX output file written in :", ARGV['output'])

    # If no entry specified
    else:
        print("No entry specified.")
        print(usage)
