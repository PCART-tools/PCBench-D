def _lexsort_indexer(keys, orders=None, na_position='last'):
    labels = []
    shape = []
    if isinstance(orders, bool):
        orders = [orders] * len(keys)
    elif orders is None:
        orders = [True] * len(keys)

    for key, order in zip(keys, orders):

        # we are already a Categorical
        if is_categorical_dtype(key):
            c = key

        # create the Categorical
        else:
            c = Categorical(key, ordered=True)

        if na_position not in ['last', 'first']:
            raise ValueError('invalid na_position: {!r}'.format(na_position))

        n = len(c.categories)
        codes = c.codes.copy()

        mask = (c.codes == -1)
        if order:  # ascending
            if na_position == 'last':
                codes = np.where(mask, n, codes)
            elif na_position == 'first':
                codes += 1
        else:  # not order means descending
            if na_position == 'last':
                codes = np.where(mask, n, n - codes - 1)
            elif na_position == 'first':
                codes = np.where(mask, 0, n - codes)
        if mask.any():
            n += 1

        shape.append(n)
        labels.append(codes)

    return _indexer_from_factorized(labels, shape)
