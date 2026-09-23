@_copy_docstring_and_deprecators(Axes.errorbar)
def errorbar(
        x, y, yerr=None, xerr=None, fmt='', ecolor=None,
        elinewidth=None, capsize=None, barsabove=False, lolims=False,
        uplims=False, xlolims=False, xuplims=False, errorevery=1,
        capthick=None, *, data=None, **kwargs):
    return gca().errorbar(
        x, y, yerr=yerr, xerr=xerr, fmt=fmt, ecolor=ecolor,
        elinewidth=elinewidth, capsize=capsize, barsabove=barsabove,
        lolims=lolims, uplims=uplims, xlolims=xlolims,
        xuplims=xuplims, errorevery=errorevery, capthick=capthick,
        **({"data": data} if data is not None else {}), **kwargs)
