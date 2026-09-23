def check_for_nonfusible_fancy_indexing(fancy, normal):
    # Check for fancy indexing and normal indexing, where the fancy
    # indexed dimensions != normal indexed dimensions with integers. E.g.:
    # disallow things like:
    # x[:, [1, 2], :][0, :, :] -> x[0, [1, 2], :] or
    # x[0, :, :][:, [1, 2], :] -> x[0, [1, 2], :]
    for f, n in zip_longest(fancy, normal, fillvalue=slice(None)):
        if type(f) is not list and isinstance(n, int):
            raise NotImplementedError("Can't handle normal indexing with "
                                      "integers and fancy indexing if the "
                                      "integers and fancy indices don't "
                                      "align with the same dimensions.")
