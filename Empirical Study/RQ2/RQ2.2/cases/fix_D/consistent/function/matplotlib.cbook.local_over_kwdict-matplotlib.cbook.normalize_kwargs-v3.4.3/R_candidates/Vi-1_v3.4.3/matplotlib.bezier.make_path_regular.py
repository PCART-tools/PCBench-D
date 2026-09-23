@_api.deprecated(
    "3.3", alternative="Path.cleaned() and remove the final STOP if needed")
def make_path_regular(p):
    """
    If the ``codes`` attribute of `.Path` *p* is None, return a copy of *p*
    with ``codes`` set to (MOVETO, LINETO, LINETO, ..., LINETO); otherwise
    return *p* itself.
    """
    from .path import Path
    c = p.codes
    if c is None:
        c = np.full(len(p.vertices), Path.LINETO, dtype=Path.code_type)
        c[0] = Path.MOVETO
        return Path(p.vertices, c)
    else:
        return p
