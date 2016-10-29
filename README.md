# mdConvert
Tool to convert .md to .tex

**What's handled :**
  - bold, italic, strikethrough
  - code (inline with `\verb` and block with `lstlistings`)
  - itemize and enumerate with a maximum of 4 levels (can be increased), however those two can't mix with each other
  - tables
  - quotations (inline and block, with or without a reference)
  - links (can be improved though, c.f. Issue)

**TO-DO :**
  - Footnote references
  - Images

# mdConvert's help

```raw
mdConvert help
Full version

Usage :
    main.py <input> <options> (normal use of the function, provides a fresh .tex document)
    main.py --help (to get this text exactly)

Options :    
    -o : shortcut for --output
    --ouput <output> : output file name (same as input file name by default)

    -d : shortcut for --date
    --date <date> : date of the document (none by default)

    -a : shortcut for --author
    --author <author> : author of the document (none by default)

    -t : shortcut for --title
    --title <title> : title of the document (none by default)

    -c : shortcut for --documentclass
    --documentclass <class> : document class (article by default)

    -p : shortcut for --packages
    --packages <pcks> : list of additionnal packages with syntax 
                        {[options1]{package1},[options2]{package2},...}
                        (none by default)

    -T : shortcut for --tableofcontents
    --tableofcontents : if a table of contents is needed ('on' by default)

    -m : shortcut for --minted ('off' by default) (/!\ HAS NOT BEEN IMPLEMENTED YET)
    --minted : if the code should be colored with minted (requires Pygments and --shell-escape option to compile)
```
