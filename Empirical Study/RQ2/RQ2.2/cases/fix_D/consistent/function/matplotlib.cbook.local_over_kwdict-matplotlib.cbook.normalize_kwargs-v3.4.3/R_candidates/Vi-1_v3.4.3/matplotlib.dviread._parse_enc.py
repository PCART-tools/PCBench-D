def _parse_enc(path):
    r"""
    Parses a \*.enc file referenced from a psfonts.map style file.
    The format this class understands is a very limited subset of PostScript.

    Parameters
    ----------
    path : os.PathLike

    Returns
    -------
    list
        The nth entry of the list is the PostScript glyph name of the nth
        glyph.
    """
    no_comments = re.sub("%.*", "", Path(path).read_text(encoding="ascii"))
    array = re.search(r"(?s)\[(.*)\]", no_comments).group(1)
    lines = [line for line in array.split() if line]
    if all(line.startswith("/") for line in lines):
        return [line[1:] for line in lines]
    else:
        raise ValueError(
            "Failed to parse {} as Postscript encoding".format(path))
