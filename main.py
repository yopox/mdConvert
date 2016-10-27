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
    'tableofcontents': 'ON',
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
        '--title': 'title',
        '-c': 'documentclass',
        '--documentclass': 'documentclass',
        '-T': 'tableofcontents',
        '--tableofcontents': 'tableofcontents',
    }

    # traitement des options
    for i in range(2, len(sys.argv)):
        if sys.argv[i] in options and i + 1 < len(sys.argv):
            ARGV[options[sys.argv[i]]] = sys.argv[i + 1]

def parse_block_code(paragraph):
        #TODO
        paragraph = re.sub(r"[é]", r"e", paragraph)
        # Ocaml specific code block
        paragraph = re.sub(r"[`]{3}[O|o](?P<g>(.*))",
                        r"\\lstset{language=\g<g>}\n\\begin{lstlisting}", paragraph)
        # Raw code block (no color)
        paragraph = re.sub(r"[`]{3}raw", r"\\begin{lstlisting}", paragraph)
        # Non breaking raw code block (no color)
        if re.match(r"[`]{3}nbraw", paragraph):
            paragraph = re.sub(r"[`]{3}nbraw", r"\\begin{figure}[!htbp]\n\\centering\n\\begin{tabular}{c}\n\\begin{lstlisting}\n", paragraph)
            nonBreakingBlock = True
        # Generic code block
        paragraph = re.sub(r"^[`]{3}(?P<g>(.{1,}))",
                        r"\\lstset{language=\g<g>}\n\\begin{lstlisting}", paragraph)
        # Code block end
        if re.match(r"^[`]{3}", paragraph):
            if nonBreakingBlock:
                paragraph = re.sub(r"^[`]{3}", r"\\end{lstlisting}\n\end{tabular}\n\\end{figure}\n", paragraph)
                nonBreakingBlock = False
            else:
                paragraph = re.sub(r"^[`]{3}", r"\\end{lstlisting}", paragraph)


def parse(paragraph):
    if paragraph[0] = '`':
        paragraph = re.sub(r"`(?P<code>)`", r"\\verb`\g<code>`")
    else:
        paragraph = re.sub(r"^[#]{6} (?P<g>(.*))", r"\\subparagraph{\g<g>}", paragraph)
        paragraph = re.sub(r"^[#]{5} (?P<g>(.*))", r"\\paragraph{\g<g>}", paragraph)
        paragraph = re.sub(r"^[#]{4} (?P<g>(.*))", r"\\subsubsection{\g<g>}", paragraph)
        paragraph = re.sub(r"^[#]{3} (?P<g>(.*))", r"\\subsection{\g<g>}", paragraph)
        paragraph = re.sub(r"^[#]{2} (?P<g>(.*))", r"\\section{\g<g>}", paragraph)
        paragraph = re.sub(r"^[#]{1} (?P<g>(.*))", r"\\chapter{\g<g>}", paragraph)

        # Horizontal line
        paragraph = re.sub(r"^[-\*_]{3,}", "\\hrulefill\n", paragraph)

        # Remove decoration
        paragraph = re.sub(r"\* \* \*", r"", paragraph)

        #### Distinguishing LaTeX from normal text
        fragments = re.split(r"(\$(?:(?!\$)(?:.|\n))*\$|\\\[(?:(?!(?:\\[|\\]))(?:.|\n))*\\\])", paragraph)
        paragraph = ""

        for fragment in fragments:
            if fragment[0] not in (r'$', r'\['):
                # Bold
                fragment = re.sub(r"\*\*(?P<bold>(?:(?!\*\*)(?:.|\n))*)\*\*",
                                   r"\\textbf{\g<bold>}", fragment)
                # Italic
                fragment = re.sub(r"_(?P<it>(?:(?!_)(?:.|\n))*)_",
                                   r"\\textbf{\g<it>}", fragment)
                # Strikethrough
                fragment = re.sub(r"[~]{2}(?P<strike>(.[^~]*))[~]{2}", r"(\g<strike>)", fragment)

                # Links
                # LaTeX math mode uses []()
                # Links like "[This is google](http://www.google.com)"
                paragraph = re.sub(r"""\[(?P<text>.*)\]\((?P<link>[^ ]*)( ".*")?\)""",
                                "\\href{\g<link>}{\g<text>}", paragraph)
                # Links like "<http://www.google.com>"
                paragraph = re.sub(
                    r"\<(?P<link>https?://[^ ]*)\>", "\\href{\g<link>}{\g<link>}", paragraph)
                # Links like " http://www.google.com "
                paragraph = re.sub(
                    r" (?P<link>https?://[^ ]*) ", " \\href{\g<link>}{\g<link>} ", paragraph)

        # Reassembling fragments
        for fragment in fragments:
            paragraph += fragment

        # New line
        paragraph = re.sub(r"[ ]*<br>", r" \\newline", paragraph)
        
        # Trees
        paragraph = re.sub(
            r"<!\-{2} TREE ([^-]*) \-{2}>[ \t]*\n?", tree, paragraph)
        
        # Comments
        paragraph = re.sub(
            r"<!(\-{2}(?P<comment>[^-]*)\-{2})*> ?\n?", "% \g<comment>\n", paragraph)

        # Quotes
        def quote_parse(matchObj):
            out = r"\n\\medskip\n\\begin{displayquote}\n\n"
            for q in matchObj.groups():
                out += q + r"\n\n"
            out += "\\end{displayquote}\n\\medskip\n"
            return out
        if re.match(r"(?:^>|\n>) *(.)*", paragraph):
            paragraph = re.sub(
                r"(?:^>|\n>) ((?:[^\n])*)", quote_parse, paragraph)

        # Itemize
        def itemize_parse(matchObj):
            itemize = matchObj.group(0)
            itemize = re.sub(r"^\n(?P<remainder>(.*))", r"\g<remainder>")
            out = r"\\begin{itemize}\n"
            for item in re.findall(r"(?:^[ ]{4}+|\n[ ]{4}+)-([^\n]*)", itemize):
                out += r"item[$bullet$] " + item + '\n'
            itemize += r"\end{itemize]"
        for i in range(4, 0, -1):
            paragraph = re.sub(r"((?:(?:^[ ]{4}+{" + str(i) + r"}|\n[ ]{4}+{" + str(i) + r"})- (?:(?:[^\n])*))+)", itemize_parse, paragraph)

        # Enumerate
        def enumerate_parse(matchObj):
            enum = matchObj.group(0)
            enum = re.sub(r"^\n(?P<remainder>(.*))", r"\g<remainder>")
            out = r"\\begin{enumerate}\n"
            for num in re.findall(r"(?:^[ ]{4}+|\n[ ]{4}+)[0-9]+\. ([^\n]*)", enum):
                out += r"item " + item + '\n'
            enum += r"\end{enumerate]"
        for i in range(4, 0, -1):
            paragraph = re.sub(r"((?:(?:^[ ]{4}+{" + str(i) + r"}|\n[ ]{4}+{" + str(i) + r"})[0-9]+\. (?:(?:[^\n])*))+)", enumerate_parse, paragraph)
    return paragraph


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

def tree(chaine):
    __nodes = chaine.group(1).split()
    if len(__nodes) % 2:
        return ""
    nodes = [[__nodes[2 * i], __nodes[2 * i + 1]] for i in range(len(__nodes) >> 1)]
    l = len(nodes)
    print(nodes)
    out_str = "\\begin{tikzpicture}[nodes={circle, draw}]\n\\graph[binary tree layout, fresh nodes]{\n"
    def get_tree():
        def aux(i, depth):
            if nodes[i][0] == 'F':
                return ('"' + nodes[i][1] + '"', i + 1)
            else:
                (g, r1) = aux(i + 1, depth + 1)
                (d, r2) = aux(r1, depth + 1)
                return ('"' + nodes[i][1] + '"' + " -- {" + g + "," + d + "}", r2)
        (ans, r) = aux(0, 1)
        if r != l:
            return ""
        else:
            return re.sub("\n ?\n", "\n", ans) + "};\n"
    out_str += get_tree() + "\\end{tikzpicture}"
    print(out_str)
    return out_str

s1 =  r"""\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[frenchb]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{tikz}
\usetikzlibrary{graphs,graphdrawing,arrows.meta}
\usegdlibrary{trees}
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

        print("Traitement de : ", inFile, "...")

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
        if ARGV['tableofcontents'] == "ON":
            output.write("\n\\tableofcontents\n")
        output.write("\n")

        chaine = r""
        
        content = inputFile.read()

        # Creation of paragraphs
        paragraphs = re.split(r"(#+ [^\n]*(?:(?!\n#+ )(?:.|\n))*)", content)

        # Splitting paragraphs into code blocks and non-code blocks
        splitted_paragraphs = [] * len(paragraphs)
        while '' in splitted_paragraphs:
            splitted_paragraphs.remove('')
        for i in range(len(paragraphs)):
            splitted_paragraphs[i] = re.split(r"```((?:[^\n])*)\n((?:(?!```).*\n*)*)\n```", paragraph[i])

        # Splitting pieces of paragraphs into inline code and normal little pieces 
        # and parsing all little pieces/pieces
        for pieces in splitted_paragraphs:
            n = len(pieces)
            if pieces[-1] = '' and n % 3 = 1:
                del pieces[-1]
            for i in range(0, n, 3):
                pieces[i] = re.split(r"(`(?:(?!`).)*`)", pieces[i])
                for little_piece in pieces[i]:
                    little_piece = parse(little_piece)
            for i in range(1, n, 3):
                pieces[i + 1] = parse_block_code(pieces[i], pieces[i + 1])
                pieces[i] = ''

        # Merging all the stuff
        for pieces in splitted_paragraphs:
            for piece in pieces:
                if type(piece) is list:
                    for little_piece in piece:
                        chaine += little_piece
                else:
                    chaine += piece


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

        print("LaTeX output file written in :", outFile)

    # If no entry specified
    else:
        print(
            '''Usage : main.py input [-o/--output output.tex] [-a/--author "M. Me"] [-d/--date today] [-t/--title "My super title"]''')
