def common_texification(text):
    r"""
    Do some necessary and/or useful substitutions for texts to be included in
    LaTeX documents.

    This distinguishes text-mode and math-mode by replacing the math separator
    ``$`` with ``\(\displaystyle %s\)``. Escaped math separators (``\$``)
    are ignored.

    The following characters are escaped in text segments: ``_^$%``
    """
    # Sometimes, matplotlib adds the unknown command \mathdefault.
    # Not using \mathnormal instead since this looks odd for the latex cm font.
    text = _replace_mathdefault(text)
    text = text.replace("\N{MINUS SIGN}", r"\ensuremath{-}")
    # split text into normaltext and inline math parts
    parts = re_mathsep.split(text)
    for i, s in enumerate(parts):
        if not i % 2:
            # textmode replacements
            s = _replace_escapetext(s)
        else:
            # mathmode replacements
            s = r"\(\displaystyle %s\)" % s
        parts[i] = s
    return "".join(parts)
