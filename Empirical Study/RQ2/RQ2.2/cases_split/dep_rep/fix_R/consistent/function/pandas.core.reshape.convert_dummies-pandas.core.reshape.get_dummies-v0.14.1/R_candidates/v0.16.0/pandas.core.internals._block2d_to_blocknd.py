def _block2d_to_blocknd(values, placement, shape, labels, ref_items):
    """ pivot to the labels shape """
    from pandas.core.internals import make_block

    panel_shape = (len(placement),) + shape

    # TODO: lexsort depth needs to be 2!!

    # Create observation selection vector using major and minor
    # labels, for converting to panel format.
    selector = _factor_indexer(shape[1:], labels)
    mask = np.zeros(np.prod(shape), dtype=bool)
    mask.put(selector, True)

    if mask.all():
        pvalues = np.empty(panel_shape, dtype=values.dtype)
    else:
        dtype, fill_value = _maybe_promote(values.dtype)
        pvalues = np.empty(panel_shape, dtype=dtype)
        pvalues.fill(fill_value)

    values = values
    for i in range(len(placement)):
        pvalues[i].flat[mask] = values[:, i]

    return make_block(pvalues, placement=placement)
