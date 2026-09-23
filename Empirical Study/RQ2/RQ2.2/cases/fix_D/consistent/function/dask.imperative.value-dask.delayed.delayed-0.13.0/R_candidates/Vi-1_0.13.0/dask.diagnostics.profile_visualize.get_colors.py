def get_colors(palette, funcs):
    """Get a dict mapping funcs to colors from palette.

    Parameters
    ----------
    palette : string
        Name of the bokeh palette to use, must be a member of
        bokeh.palettes.all_palettes.
    funcs : iterable
        Iterable of function names
    """
    palettes = import_required('bokeh.palettes', _BOKEH_MISSING_MSG)
    tz = import_required('toolz', _TOOLZ_MISSING_MSG)

    unique_funcs = list(sorted(tz.unique(funcs)))
    n_funcs = len(unique_funcs)
    palette_lookup = palettes.all_palettes[palette]
    keys = list(sorted(palette_lookup.keys()))
    index = keys[min(bisect_left(keys, n_funcs), len(keys) - 1)]
    palette = palette_lookup[index]
    # Some bokeh palettes repeat colors, we want just the unique set
    palette = list(tz.unique(palette))
    if len(palette) > n_funcs:
        # Consistently shuffle palette - prevents just using low-range
        random.Random(42).shuffle(palette)
    color_lookup = dict(zip(unique_funcs, cycle(palette)))
    return [color_lookup[n] for n in funcs]
