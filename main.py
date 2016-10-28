# -*- coding: utf-8 -*-
# Little tool to convert Markdown to cool LaTeX documents.
# Written by YoPox and Hadrien

# IMPORT
import re
import sys

ARGV = {
    'output': "output.tex",
    'input': '',
    'author': '',
    'title': '',
    'documentclass': 'report',
    'tableofcontents': 'ON',
}

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
    # # # # # # # # # # # # # #
    # Parsing blocks of code  #
    # # # # # # # # # # # # # #
    # Blocks are "encrypted" in the string and stocked in a list. Everything is merged afterwards.
    block_codes = []
    def sep_parse_block_code(matchObj):
        #TODO
        code   = matchObj.group('code')
        option = matchObj.group('option')
        block_codes.append(code)
        return r"&é(]'(-è*@|{)" + str(len(block_codes)) + r"&é(]'(-è*@|{)"
    paragraph = re.sub(r"```(?P<option>[^\n]*)\n(?P<code>(?:(?!```)(?:.|\n))*)\n```", sep_parse_block_code, paragraph)

    # # # # # # # # # # # #
    # Parsing inline code #
    # # # # # # # # # # # #
    # Inline codes are "encrypted" in the string and stocked in a list. Everything is merged afterwards.
    inline_codes = []
    def sep_parse_inline_code(matchObj):
        code = matchObj.group('code')
        inline_codes.append("\\verb`" + code + '`')
        return r'£%£%§²&' + str(len(inline_codes)) + r'£%£%§²&'
    paragraph = re.sub("`(?P<code>[^`]*)`", sep_parse_inline_code, paragraph)

    # # # # # # # # # #
    # Parsing titles  #
    # # # # # # # # # #
    # Each paragraph's string begins with some '#' so regex matches only the string's beginning
    paragraph = re.sub(r"^[#]{6} (?P<g>(.*))", r"\\subparagraph{\g<g>}", paragraph)
    paragraph = re.sub(r"^[#]{5} (?P<g>(.*))", r"\\paragraph{\g<g>}", paragraph)
    paragraph = re.sub(r"^[#]{4} (?P<g>(.*))", r"\\subsubsection{\g<g>}", paragraph)
    paragraph = re.sub(r"^[#]{3} (?P<g>(.*))", r"\\subsection{\g<g>}", paragraph)
    paragraph = re.sub(r"^[#]{2} (?P<g>(.*))", r"\\section{\g<g>}", paragraph)
    paragraph = re.sub(r"^[#]{1} (?P<g>(.*))", r"\\chapter{\g<g>}", paragraph)

    # # # # # # # # # # #
    # Horizontal lines  #
    # # # # # # # # # # #
    paragraph = re.sub(r"^[-\*_]{3,}", "\\hrulefill\n", paragraph)

    # # # # # # # # # # # #
    # Removing decoration #
    # # # # # # # # # # # #
    paragraph = re.sub(r"\* \* \*", '', paragraph)

    # # # # # # # # # # # # # # # # #
    # Operations on non-LaTeX text  #
    # # # # # # # # # # # # # # # # #
    # For bold, italic etc. LaTeX must be put aside : paragraph is splitted into LaTeX parts and non-LaTeX parts which are called fragments
    fragments = re.split(r"(\$(?:(?!\$)(?:.|\n))*\$|\\\[(?:(?!(?:\\\[|\\\]))(?:.|\n))*\\\])", paragraph)

    # Each style has it own function that checks if there are no subtle syntax problems
    for i in range(len(fragments)):
        # Bold #
        def bolden(matchObj):
            bold = matchObj.group('bold')
            left1  = re.findall(r"^~~((?!(?:~~))[^ ])|(?:(?!(?:~~))\W)~~(?:(?!(?:~~))[^ ])", bold)
            right1 = re.findall(r"(?:(?!(?:~~))[^ ])~~$|(?:(?!(?:~~))[^ ])~~(?:(?!(?:~~))\W)", bold)
            left2  = re.findall(r"^_((?!(?:_))[^ ])|(?:(?!(?:_))\W)_(?:(?!(?:_))[^ ])", bold)
            right2 = re.findall(r"(?:(?!(?:_))[^ ])_$|(?:(?!(?:_))[^ ])_(?:(?!(?:_))\W)", bold)
            print(left1, left2, right1, right2)
            if r"\begin" not in bold and r"\end" not in bold and len(left1) == len(right1) and len(left2) == len(right2):
                print("Bolden has been called with parameter " + bold + " and it is functionnal")
                return r"\textbf{" + bold + "}"
            else:
                return bold
        fragments[i] = re.sub(r"[*]{2}(?! )(?P<bold>(?:(?![*]{2})(?:.|\n))+)(?<! )[*]{2}", bolden, fragments[i])
        
        # Italic #
        def italien(matchObj):
            it = matchObj.group('it')
            left1  = re.findall(r"^\*\*((?!(?:\*\*))[^ ])|(?:(?!(?:\*\*))\W)\*\*(?:(?!(?:\*\*))[^ ])", it)
            right1 = re.findall(r"(?:(?!(?:\*\*))[^ ])\*\*$|(?:(?!(?:\*\*))[^ ])\*\*(?:(?!(?:\*\*))\W)", it)
            left2  = re.findall("^_((?!(?:_))[^ ])|(?:(?!(?:_))\W)_(?:(?!(?:_))[^ ])", it)
            right2 = re.findall("(?:(?!(?:_))[^ ])_$|(?:(?!(?:_))[^ ])_(?:(?!(?:_))\W)", it)
            if r"\begin" not in it and r"\end" not in it and len(left1) == len(right1) and len(left2) == len(right2):
                return r"\textit{" + it + "}"
            else:
                return it
        fragments[i] = re.sub(r"_(?! )(?P<it>(?:(?!_)(?:.|\n))+)(?<! )_", italien, fragments[i]) # So funny
        
        # Strikethrough #
        def striken(matchObj):
            strike = matchObj.group('strike')
            left1  = re.findall(r"^\*\*((?!(?:\*\*))[^ ])|(?:(?!(?:\*\*))\W)\*\*(?:(?!(?:\*\*))[^ ])", strike)
            right1 = re.findall(r"(?:(?!(?:\*\*))[^ ])\*\*$|(?:(?!(?:\*\*))[^ ])\*\*(?:(?!(?:\*\*))\W)", strike)
            left2  = re.findall("^~~((?!(?:~~))[^ ])|(?:(?!(?:~~))\W)~~(?:(?!(?:~~))[^ ])", strike)
            right2 = re.findall("(?:(?!(?:~~))[^ ])~~$|(?:(?!(?:~~))[^ ])~~(?:(?!(?:~~))\W)", strike)
            if r"\begin" not in strike and r"\end" not in strike and len(left1) == len(right1) and len(left2) == len(right2):
                return r"\textbf{" + strike + "}"
            else:
                return strike
        fragments[i] = re.sub(r"~~(?! )(?P<strike>(?:(?!~~)(?:.|\n))+)(?<! )~~", striken, fragments[i])

        # Links #
        # Links like "[This is google](http://www.google.com)"
        fragments[i] = re.sub(r"""\[(?P<text>.*)\]\((?P<link>[^ ]*)( ".*")?\)""",
                        "\\href{\g<link>}{\g<text>}", fragments[i])
        # Links like "<http://www.google.com>"
        fragments[i] = re.sub(
            r"\<(?P<link>https?://[^ ]*)\>", "\\href{\g<link>}{\g<link>}", fragments[i])
        # Links like " http://www.google.com "
        fragments[i] = re.sub(
            r" (?P<link>https?://[^ ]*) ", " \\href{\g<link>}{\g<link>} ", fragments[i])

    # Merging fragments
    paragraph = ''
    for fragment in fragments:
        paragraph += fragment

    # # # # # # #
    # New line  #
    # # # # # # #
    paragraph = re.sub(r"[ ]*<br>", r" \\newline", paragraph)
    
    # # # # #
    # Trees #
    # # # # #
    def tree_parse(matchObj):
        # Possible options : 
        #   - c : center
        #   - all for now
        option = matchObj.group('option')
        __nodes = matchObj.group('tree').split()
        if len(__nodes) % 2:
            return ""
        nodes = [[__nodes[2 * i], __nodes[2 * i + 1]] for i in range(len(__nodes) >> 1)]
        l = len(nodes)
        print(nodes)
        out_str = "\n\\begin{center}" if option == 'c' else ""
        out_str += "\n\\begin{tikzpicture}[nodes={circle, draw}]\n\\graph[binary tree layout, fresh nodes]{\n"
        # The package used to draw trees is TikZ and that requiers LuaLaTeX to compile (the algorithm aiming at computing distance 
        # between elements of the graphs is written in Lua)
        # The traversal is a pre-order traversal
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
        out_str += get_tree() + "\\end{tikzpicture}\n" + ("\\end{center}\n" if option == 'c' else "")
        print(out_str)
        return out_str
    paragraph = re.sub(r"<!\-\-(?P<option>[a-z]?) TREE (?P<tree>(?:(?!\-\->).)*) \-\->?", tree_parse, paragraph)
    
    # # # # # # #
    # Comments  #
    # # # # # # #
    paragraph = re.sub(r"<!\-\-(?P<comment>(?:(?!\-\->).)*)\-\->", "% \g<comment>", paragraph)

    # # # # # #
    # Quotes  #
    # # # # # #
    def quote_parse(matchObj):
        quotes = matchObj.group(0)
        quotes = re.split("(?:^|\n)> (.*)", quotes)
        out = "\n\\medskip\n\\begin{displayquote}\n"
        for quote in quotes:
            if quote != '':
                out += quote + "\n"
        out += "\\end{displayquote}\n\\medskip\n"
        return out
    paragraph = re.sub(r"(?:^>|(?<=\n)>) (?:.|\n(?=> ))*", quote_parse, paragraph)

    # # # # # #
    # Itemize #
    # # # # # #
    # Item levels are parsed in the decreasing order
    def itemize_parse(i, matchObj):
        # i : item depth
        itemize = matchObj.group(0)
        # If level is not 1 we add some space and a '-' to make the algorithm believe that the items are normal markdown items when it parses a smaller level
        out = (("    "*i + "- ") if i != 1 else "") + "\\begin{itemize}\n"
        for item in re.findall(r"(?:^(?:[ ]{4})+|\n(?:[ ]{4})+)- ((?:(?!\n[ ]{4,}- )(?:.|\n))*)", itemize):
            out += (r"\item[$\bullet$] " if item[0:min(len(item), 6)] != "\\begin" else "") + item + '\n'
        out += r"\end{itemize}"
        return out
    for i in range(4, 0, -1):
        pattern = r"(?:^[ ]{" + str(4*i) + r"}|(?<=\n)[ ]{" + str(4*i) + r"})- (?:(?!(?:\n\n|\n[ ]{0," + str(4 * i - 2) + r"}- ))(?:.|\n))*"
        paragraph = re.sub(pattern, lambda x: itemize_parse(i, x), paragraph)

    # # # # # # #
    # Enumerate #
    # # # # # # #
    def enumerate_parse(i, matchObj):
        # Same idea
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

    # # # # # # # # # #
    # Parsing tables  #
    # # # # # # # # # #
    #TODO ? Or not TODO ? That is the question
    def parse_table(m):
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
    paragraph = re.sub(r"((\|[^\n|]+)*)(\s)*\|?(\s)*((\| ?:?-+:? ?)+)\|[ \t]*\n[ \t]*((((\|([^|\n]*))*)\|?[ \t]*\n?)+)", parse_table, paragraph)
        
    
    # # # # # # # # # # # #
    # Merging inline code #
    # # # # # # # # # # # #
    def merge_inline_code(matchObj):
        return inline_codes[int(matchObj.group('i')) - 1]
    paragraph = re.sub(r"£%£%§²&(?P<i>[0-9]+)£%£%§²&", merge_inline_code, paragraph)

    # # # # # # # # # # # # # #
    # Merging blocks of code  #
    # # # # # # # # # # # # # #
    def merge_block_code(matchObj):
        return block_codes[int(matchObj.group('i')) - 1]
    paragraph = re.sub(r"&é\(\]'\(\-è\*@\|\{\)(?P<i>[0-9]+)&é\(\]'\(\-è\*@\|\{\)", merge_block_code, paragraph)
    print(paragraph)
    return paragraph


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

        # Creation of the main string
        main_string = r""
        
        # Reading the file
        contents = inputFile.read()

        # Creation of paragraphs
        paragraphs = re.split(r"(#+ [^\n]*(?:(?!\n#+ )(?:.|\n))*)", contents)

        # Parsing every paragraph and add it to the main string
        for paragraph in paragraphs:
            main_string += parse(paragraph)

        # Converting euro symbol to LaTeX command
        main_string = re.sub(r"€", "\\euro{}", main_string)

        # Formating line breaks
        main_string = re.sub(r"\\medskip", r"\n\\medskip\n", main_string)
        main_string = re.sub(r"[\n]{2,}", r"\n\n", main_string)
        main_string = re.sub(r"\\medskip[\n]{1,}\\medskip", r"\n\\medskip\n", main_string)

        output.write(main_string)

        output.write("\n")
        output.write(r"\end{document}")

        inputFile.close()
        output.close()

        print("LaTeX output file written in :", outFile)

    # If no entry specified
    else:
        print(
            '''Usage : main.py input [-o/--output output.tex] [-a/--author "M. Me"] [-d/--date today] [-t/--title "My super title"]''')
