def form_blocks(arrays, names, axes):
    # put "leftover" items in float bucket, where else?
    # generalize?
    float_items = []
    complex_items = []
    int_items = []
    bool_items = []
    object_items = []
    sparse_items = []
    datetime_items = []
    datetime_tz_items = []
    cat_items = []
    extra_locs = []

    names_idx = Index(names)
    if names_idx.equals(axes[0]):
        names_indexer = np.arange(len(names_idx))
    else:
        assert names_idx.intersection(axes[0]).is_unique
        names_indexer = names_idx.get_indexer_for(axes[0])

    for i, name_idx in enumerate(names_indexer):
        if name_idx == -1:
            extra_locs.append(i)
            continue

        k = names[name_idx]
        v = arrays[name_idx]

        if is_sparse(v):
            sparse_items.append((i, k, v))
        elif issubclass(v.dtype.type, np.floating):
            float_items.append((i, k, v))
        elif issubclass(v.dtype.type, np.complexfloating):
            complex_items.append((i, k, v))
        elif issubclass(v.dtype.type, np.datetime64):
            if v.dtype != _NS_DTYPE:
                v = tslib.cast_to_nanoseconds(v)

            if is_datetimetz(v):
                datetime_tz_items.append((i, k, v))
            else:
                datetime_items.append((i, k, v))
        elif is_datetimetz(v):
            datetime_tz_items.append((i, k, v))
        elif issubclass(v.dtype.type, np.integer):
            if v.dtype == np.uint64:
                # HACK #2355 definite overflow
                if (v > 2**63 - 1).any():
                    object_items.append((i, k, v))
                    continue
            int_items.append((i, k, v))
        elif v.dtype == np.bool_:
            bool_items.append((i, k, v))
        elif is_categorical(v):
            cat_items.append((i, k, v))
        else:
            object_items.append((i, k, v))

    blocks = []
    if len(float_items):
        float_blocks = _multi_blockify(float_items)
        blocks.extend(float_blocks)

    if len(complex_items):
        complex_blocks = _multi_blockify(complex_items)
        blocks.extend(complex_blocks)

    if len(int_items):
        int_blocks = _multi_blockify(int_items)
        blocks.extend(int_blocks)

    if len(datetime_items):
        datetime_blocks = _simple_blockify(datetime_items, _NS_DTYPE)
        blocks.extend(datetime_blocks)

    if len(datetime_tz_items):
        dttz_blocks = [make_block(array,
                                  klass=DatetimeTZBlock,
                                  fastpath=True,
                                  placement=[i], )
                       for i, _, array in datetime_tz_items]
        blocks.extend(dttz_blocks)

    if len(bool_items):
        bool_blocks = _simple_blockify(bool_items, np.bool_)
        blocks.extend(bool_blocks)

    if len(object_items) > 0:
        object_blocks = _simple_blockify(object_items, np.object_)
        blocks.extend(object_blocks)

    if len(sparse_items) > 0:
        sparse_blocks = _sparse_blockify(sparse_items)
        blocks.extend(sparse_blocks)

    if len(cat_items) > 0:
        cat_blocks = [make_block(array, klass=CategoricalBlock, fastpath=True,
                                 placement=[i])
                      for i, _, array in cat_items]
        blocks.extend(cat_blocks)

    if len(extra_locs):
        shape = (len(extra_locs),) + tuple(len(x) for x in axes[1:])

        # empty items -> dtype object
        block_values = np.empty(shape, dtype=object)
        block_values.fill(np.nan)

        na_block = make_block(block_values, placement=extra_locs)
        blocks.append(na_block)

    return blocks
