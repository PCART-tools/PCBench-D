def to_hex(c, keep_alpha=False):
    """
    Convert *c* to a hex color.

    Uses the ``#rrggbb`` format if *keep_alpha* is False (the default),
    ``#rrggbbaa`` otherwise.
    """
    c = to_rgba(c)
    if not keep_alpha:
        c = c[:3]
    return "#" + "".join(format(int(round(val * 255)), "02x") for val in c)
