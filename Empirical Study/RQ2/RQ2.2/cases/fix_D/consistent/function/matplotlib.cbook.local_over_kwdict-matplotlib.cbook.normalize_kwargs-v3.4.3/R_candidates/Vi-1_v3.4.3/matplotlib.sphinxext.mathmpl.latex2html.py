def latex2html(node, source):
    inline = isinstance(node.parent, nodes.TextElement)
    latex = node['latex']
    fontset = node['fontset']
    name = 'math-{}'.format(
        hashlib.md5((latex + fontset).encode()).hexdigest()[-10:])

    destdir = Path(setup.app.builder.outdir, '_images', 'mathmpl')
    destdir.mkdir(parents=True, exist_ok=True)
    dest = destdir / f'{name}.png'

    depth = latex2png(latex, dest, fontset)

    if inline:
        cls = ''
    else:
        cls = 'class="center" '
    if inline and depth != 0:
        style = 'style="position: relative; bottom: -%dpx"' % (depth + 1)
    else:
        style = ''

    return (f'<img src="{setup.app.builder.imgpath}/mathmpl/{name}.png"'
            f' {cls}{style}/>')
