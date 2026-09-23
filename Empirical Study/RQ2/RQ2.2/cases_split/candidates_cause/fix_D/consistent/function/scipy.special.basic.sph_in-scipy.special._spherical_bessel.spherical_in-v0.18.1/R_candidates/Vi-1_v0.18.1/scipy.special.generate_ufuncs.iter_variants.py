def iter_variants(inputs, outputs):
    """
    Generate variants of UFunc signatures, by changing variable types,
    within the limitation that the corresponding C types casts still
    work out.

    This does not generate all possibilities, just the ones required
    for the ufunc to work properly with the most common data types.

    Parameters
    ----------
    inputs, outputs : str
        UFunc input and output signature strings

    Yields
    ------
    new_input, new_output : str
        Modified input and output strings.
        Also the original input/output pair is yielded.

    """
    maps = [
        # always use long instead of int (more common type on 64-bit)
        ('i', 'l'),
    ]

    # float32-preserving signatures
    if not ('i' in inputs or 'l' in inputs):
        # Don't add float32 versions of ufuncs with integer arguments, as this
        # can lead to incorrect dtype selection if the integer arguments are
        # arrays, but float arguments are scalars.
        # For instance sph_harm(0,[0],0,0).dtype == complex64
        # This may be a Numpy bug, but we need to work around it.
        # cf. gh-4895, https://github.com/numpy/numpy/issues/5895
        maps = maps + [(a + 'dD', b + 'fF') for a, b in maps]

    # do the replacements
    for src, dst in maps:
        new_inputs = inputs
        new_outputs = outputs
        for a, b in zip(src, dst):
            new_inputs = new_inputs.replace(a, b)
            new_outputs = new_outputs.replace(a, b)
        yield new_inputs, new_outputs
