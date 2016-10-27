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
    if paragraph[0] == '`':
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

        # Distinguishing LaTeX from normal text
        fragments = re.split(r"(\$(?:(?!\$)(?:.|\n))*\$|\\\[(?:(?!(?:\\[|\\]))(?:.|\n))*\\\])", paragraph)

        for i in range(len(fragments)):
            if fragments[i][0] not in (r'$', r'\['):
                # Bold
                def bolden(matchObj):
                    bold = matchObj.goup('bold')
                    if r"\begin" not in bold and r"\end" not in bold:
                        if len(re.findall("^_((?!(?:_))[^ ])|(?:(?!(?:_))[ \n])_(?:(?!(?:_))[^ ])|(?:(?!(?:_))[^ ])_$|(?:(?!(?:_))[^ ])_(?:(?!(?:_))[ \n])", bold)) % 2 and
                           len(re.findall("^~~((?!(?:~~))[^ ])|(?:(?!(?:~~))[ \n])~~(?:(?!(?:~~))[^ ])|(?:(?!(?:~~))[^ ])~~$|(?:(?!(?:~~))[^ ])~~(?:(?!(?:~~))[ \n])", bold)) % 2:
                           return r"\textbf{" + bold + "}"
                    else:
                        return bold
                fragments[i] = re.sub(r"(?:\n| )\*\*(?P<bold>(?:(?!\*\*)(?:.|\n))*)\*\*(?:\n| )",
                                    bolden, fragments[i])
                # Italic
                def italien(matchObj):
                    it = matchObj.goup('it')
                    if r"\begin" not in it and r"\end" not in it:
                        if len(re.findall("^\*\*((?!(?:\*\*))[^ ])|(?:(?!(?:\*\*))[ \n])\*\*(?:(?!(?:\*\*))[^ ])|(?:(?!(?:\*\*))[^ ])\*\*$|(?:(?!(?:\*\*))[^ ])\*\*(?:(?!(?:\*\*))[ \n])", it)) % 2 and
                           len(re.findall("^~~((?!(?:~~))[^ ])|(?:(?!(?:~~))[ \n])~~(?:(?!(?:~~))[^ ])|(?:(?!(?:~~))[^ ])~~$|(?:(?!(?:~~))[^ ])~~(?:(?!(?:~~))[ \n])", it)) % 2:
                           return r"\textbf{" + it + "}"
                    else:
                        return it
                fragments[i] = re.sub(r"(?:\n| )_(?P<it>(?:(?!_)(?:.|\n))*)_(?:\n| )",
                                    italien, fragments[i]) # So funny
                # Strikethrough
                def striken(matchObj):
                    strike = matchObj.goup('strike')
                    if r"\begin" not in strike and r"\end" not in strike:
                        if len(re.findall("^\*\*((?!(?:\*\*))[^ ])|(?:(?!(?:\*\*))[ \n])\*\*(?:(?!(?:\*\*))[^ ])|(?:(?!(?:\*\*))[^ ])\*\*$|(?:(?!(?:\*\*))[^ ])\*\*(?:(?!(?:\*\*))[ \n])", strike)) % 2 and
                           len(re.findall("^_((?!(?:_))[^ ])|(?:(?!(?:_))[ \n])_(?:(?!(?:_))[^ ])|(?:(?!(?:_))[^ ])_$|(?:(?!(?:_))[^ ])_(?:(?!(?:_))[ \n])", strike)) % 2:
                           return r"\textbf{" + strike + "}"
                    else:
                        return strike
                fragments[i] = re.sub(r"(?:\n| )~~(?P<strike>(?:(?!~~)(?:.|\n))*)~~(?:\n| )", 
                                    striken, fragments[i])

                # Links
                # LaTeX math mode uses []()
                # Links like "[This is google](http://www.google.com)"
                fragments[i] = re.sub(r"""\[(?P<text>.*)\]\((?P<link>[^ ]*)( ".*")?\)""",
                                "\\href{\g<link>}{\g<text>}", fragments[i])
                # Links like "<http://www.google.com>"
                fragments[i] = re.sub(
                    r"\<(?P<link>https?://[^ ]*)\>", "\\href{\g<link>}{\g<link>}", fragments[i])
                # Links like " http://www.google.com "
                fragments[i] = re.sub(
                    r" (?P<link>https?://[^ ]*) ", " \\href{\g<link>}{\g<link>} ", fragments[i])

        # Reassembling fragments
        paragraph = ''
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
            quotes = matchObj.group(0)
            quotes = re.sub(r"^\n(?P<remainder>(.*))", r"\g<remainder>", quotes)
            quotes = re.split("\n> ((?:(?!\n).)*)", quotes)
            out = "\n\\medskip\n\\begin{displayquote}\n\n"
            for quote in quotes:
                if quote != '':
                    out += quote + "\n\n"
            out += "\\end{displayquote}\n\\medskip\n"
            return out
        paragraph = re.sub(
            r"(?:(?:^>|\n>) (?:(?:[^\n])*))+", quote_parse, paragraph)

        # Itemize
        def itemize_parse(i, matchObj):
            itemize = matchObj.group(0)
            out = (("    "*i + "- ") if i != 1 else "") + "\\begin{itemize}\n"
            for item in re.findall(r"(?:^(?:[ ]{4})+|\n(?:[ ]{4})+)- ((?:(?!\n[ ]{4,}- )(?:.|\n))*)", itemize):
                out += (r"\item[$\bullet$] " if item[0:min(len(item), 6)] != "\\begin" else "") + item + '\n'
            out += r"\end{itemize}"
            return out
        for i in range(4, 0, -1):
            #pattern = r"(?:^[ ]{" + str(4*i) + r"}|(?<=\n)[ ]{" + str(4*i) + r"})- (?:(?!(?:\n\n|\n[ ]{" + str(4 * i + 4) + r",}- |\n[ ]{0," + str(4 * i - 2) + r"}- ))(?:.|\n))*"
            pattern = r"(?:^[ ]{" + str(4*i) + r"}|(?<=\n)[ ]{" + str(4*i) + r"})- (?:(?!(?:\n\n|\n[ ]{0," + str(4 * i - 2) + r"}- ))(?:.|\n))*"
            paragraph = re.sub(pattern, lambda x: itemize_parse(i, x), paragraph)

        # Enumerate
        def enumerate_parse(i, matchObj):
            enum = matchObj.group(0)
            out = (("    "*i + "1. ") if i != 1 else "") + "\\begin{enumerate}\n"
            for item in re.findall(r"(?:^(?:[ ]{4})+|\n(?:[ ]{4})+)[0-9]+\. ((?:(?!\n[ ]{4,}[0-9]+\. )(?:.|\n))*)", enum):
                out += (r"\item " if item[0:min(len(item), 6)] != "\\begin" else "") + item + '\n'
            out += r"\end{enumerate}"
            return out
        for i in range(4, 0, -1):
            #pattern = r"(?:^[ ]{" + str(4*i) + r"}|(?<=\n)[ ]{" + str(4*i) + r"})[0-9]+\. (?:(?!(?:\n\n|\n[ ]{" + str(4 * i + 4) + r",}[0-9]+\. |\n[ ]{0," + str(4 * i - 2) + r"}[0-9]+\. ))(?:.|\n))*"
            pattern = r"(?:^[ ]{" + str(4*i) + r"}|(?<=\n)[ ]{" + str(4*i) + r"})[0-9]+\. (?:(?!(?:\n\n|\n[ ]{0," + str(4 * i - 2) + r"}[0-9]+\. ))(?:.|\n))*"
            paragraph = re.sub(pattern, lambda x: enumerate_parse(i, x), paragraph)
        print(paragraph)
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
            if pieces[-1] == '' and n % 3 == 1:
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
