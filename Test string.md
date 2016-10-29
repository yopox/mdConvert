## Foo bar
### Random text
Lorem ipsum dolor sit amet, consectetur **adipiscing elit**. Suspendisse sollicitudin mi consequat, _imperdiet enim sit amet_, sagittis metus. Suspendisse eleifend ~~consectetur nisl~~, a efficitur dolor feugiat vitae. "Suspendisse facilisis 'nisl' quam", sed suscipit enim suscipit vel. Vivamus quis molestie turpis. Nullam at hendrerit est, non varius sapien. Mauris nec diam sapien. Nam lacinia urna eget `neque` mattis tristique. Donec et ante enim.

- Ut sed metus quis mi posuere gravida.
- Praesent accumsan, leo et sollicitudin vehicula
    - nisi est vehicula quam, ac euismod lacus nulla sed nisi.
        - Fusce felis sapien,
        - suscipit a libero quis,
    - ultricies sagittis elit.
    - Vestibulum pellentesque
- condimentum enim vitae luctus.
- In tincidunt et odio a maximus.
  Curabitur nec nibh in ex scelerisque tristique.
  Nunc convallis leo eu velit interdum, nec volutpat erat porta.

```python
def itemize_parse(i, matchObj):
    # i : item depth
    itemize = matchObj.group(0)
    # If level is not 1 we add some space and a '-' to make the algorithm believe that the items are normal markdown items when it parses a smaller level
    out = (("    "*i + "- ") if i != 1 else "") + "\\begin{itemize}\n"
    for item in re.findall(r"(?:^(?:[ ]{4})+|\n(?:[ ]{4})+)- ((?:(?!\n[ ]{4,}- )(?:.|\n))*)", itemize):
        out += (r"\item[$\bullet$] " if item[0:min(len(item), 6)] != "\\begin" else "") + item + '\n'
    out += r"\end{itemize}"
    return out
```

```ocaml
let rec fact n = match n with
  | 0 -> 1
  | _ -> n * fact (n-1);;
```

### This has no sens
Vivamus sed ante sed felis tincidunt dictum sed quis massa :
> Nulla purus lorem, placerat in elit dapibus, mattis bibendum sem.
> In a mattis augue, ut venenatis mi.
(Plato, in his song Macarena)

**Suspendisse efficitur nunc urna, ut mollis dolor tempus eget.
Ut suscipit ultrices libero a rhoncus.
Vivamus posuere volutpat lorem sit amet ullamcorper.**

1. Cras a rhoncus nisi,
1. in aliquam nisi.
1. Curabitur vulputate massa id tristique gravida.
1. Vestibulum a maximus lacus.

| TEST                 | Hi   | this      | is            | a           |
|----------------------|------|-----------|---------------|-------------|
| $x\in\mathbb{R}$ !!! | ...  | é"'(-è_ç | **hello**     | Lorem ipsum |
| je                   | n'ai | plus      | d'inspiration | ...         |
| Allez                | une  | dernière  | ligne         | !!!         |

"hello 'hello" hello'

## Last part !!

Phasellus nisl magna, hendrerit quis libero quis, finibus eleifend odio. Ut tristique consectetur turpis non fermentum. In libero nibh, mattis in molestie a, egestas ac mauris. Quisque ac tempus lorem, vitae imperdiet nibh. Maecenas eu vehicula nunc. Nam a cursus augue. Praesent eu accumsan leo.

Phasellus mi lorem, interdum et neque ac, porta varius ex. Nulla sollicitudin est laoreet sodales porta. Donec ut felis tortor. Vestibulum sed nisi vulputate, tristique lectus et, tempus mauris. Fusce gravida odio eget erat imperdiet iaculis. Praesent sit amet volutpat purus, ac faucibus lacus. Vivamus sed dignissim lacus. Etiam placerat enim ullamcorper magna lobortis, vitae tempus mauris tincidunt. Mauris commodo vulputate laoreet. Phasellus sit amet dictum elit. In vestibulum felis lorem, non suscipit nulla sollicitudin a.

Phasellus aliquam varius lorem in sodales. Morbi pellentesque elit sit amet quam ultrices, vel rhoncus ligula accumsan. Mauris sodales, risus mollis facilisis venenatis, augue enim consectetur sem, quis tempus nibh nulla eget ipsum. Ut pellentesque nunc elit, quis tempus urna auctor in. Sed consectetur, dolor quis elementum vehicula, leo orci ullamcorper mi, vel bibendum diam tortor non ex. Quisque posuere placerat nibh, nec ullamcorper odio. Donec nulla lacus, rutrum ac urna nec, eleifend sagittis justo. Vivamus eu justo vitae diam imperdiet porta. Integer vehicula velit ac vehicula rhoncus. Sed vel tellus eleifend, placerat nunc eu, malesuada libero. Quisque sagittis laoreet cursus. Suspendisse finibus nulla lacus, sit amet posuere risus dignissim a. Integer id tellus ipsum. Duis mollis mauris at neque finibus volutpat a sit amet quam. Donec ut efficitur metus. Integer convallis in risus sit amet faucibus.
