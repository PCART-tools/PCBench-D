def get_fontspec():
    """Build fontspec preamble from rc."""
    latex_fontspec = []
    texcommand = mpl.rcParams["pgf.texsystem"]

    if texcommand != "pdflatex":
        latex_fontspec.append("\\usepackage{fontspec}")

    if texcommand != "pdflatex" and mpl.rcParams["pgf.rcfonts"]:
        families = ["serif", "sans\\-serif", "monospace"]
        commands = ["setmainfont", "setsansfont", "setmonofont"]
        for family, command in zip(families, commands):
            # 1) Forward slashes also work on Windows, so don't mess with
            # backslashes.  2) The dirname needs to include a separator.
            path = pathlib.Path(fm.findfont(family))
            latex_fontspec.append(r"\%s{%s}[Path=\detokenize{%s}]" % (
                command, path.name, path.parent.as_posix() + "/"))

    return "\n".join(latex_fontspec)
