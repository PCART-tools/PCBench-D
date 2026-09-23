def get_colors(palette, funcs):
    """Get a dict mapping funcs to colors from palette.

    Parameters
    ----------
    palette : string
        Name of the palette. Must be a key in bokeh.palettes.brewer
    funcs : iterable
        Iterable of function names
    """
    palettes = import_required('bokeh.palettes', _BOKEH_MISSING_MSG)
    tz = import_required('toolz', _TOOLZ_MISSING_MSG)

    unique_funcs = list(sorted(tz.unique(funcs)))
    n_funcs = len(unique_funcs)
    palette_lookup = palettes.brewer[palette]
    keys = list(palette_lookup.keys())
    low, high = min(keys), max(keys)
    if n_funcs > high:
        colors = cycle(palette_lookup[high])
    elif n_funcs < low:
        colors = palette_lookup[low]
    else:
        colors = palette_lookup[n_funcs]
    color_lookup = dict(zip(unique_funcs, colors))
    return [color_lookup[n] for n in funcs]
