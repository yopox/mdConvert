# -*- coding: utf-8 -*-
# Little tool to convert Markdown to cool LaTeX documents.
# Written by YoPox on 09/18/2016

import re

### Definitions

def parse(chaine):
    chaine = re.sub(r"[*]{2}(?P<g>(.*))[*]{2}", r"\\textbf{\g<g>}", chaine)
    chaine = re.sub(r"<br>", r"\\newline", chaine)
    chaine = re.sub(r"\* \* \*", r"", chaine)
    chaine = re.sub(r"^[#]{6} (?P<g>(.*))", r"\\subparagraph{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{5} (?P<g>(.*))", r"\\paragraph{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{4} (?P<g>(.*))", r"\\subsubsection{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{3} (?P<g>(.*))", r"\\subsection{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{2} (?P<g>(.*))", r"\\section{\g<g>}", chaine)
    chaine = re.sub(r"^[#]{1} (?P<g>(.*))", r"\\chapter{\g<g>}", chaine)
    chaine = re.sub(r"^```(?P<g>(.{1,}))", r"\\lstset{language=\g<g>}\n\\begin{lstlisting}", chaine)
    chaine = re.sub(r"^```", r"\\end{lstlisting}", chaine)
    chaine = re.sub(r"^-(?P<g>(.*))", r"$\cdot$\g<g>\\\\", chaine)
    return chaine

s1 =  r"""\documentclass{report}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[frenchb]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{listings}
\usepackage{mathrsfs}"""

s2 = r"""\begin{document}
\nocite{*}

\maketitle
\tableofcontents"""

### Actual stuff

inputFile = open(input("File to convert : "), 'r')
output = open('output.tex', 'w')

output.seek(0)
output.write(s1)
output.write("\n\n")
output.write(r"\author{" + input("Author : ") + "}")
output.write("\n")
output.write(r"\title{" + input("Title : ") + "}")
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
