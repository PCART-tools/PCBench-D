def _interleaved_dtype(blocks):
    if not len(blocks):
        return None

    counts = defaultdict(lambda: [])
    for x in blocks:
        counts[type(x)].append(x)

    def _lcd_dtype(l):
        """ find the lowest dtype that can accomodate the given types """
        m = l[0].dtype
        for x in l[1:]:
            if x.dtype.itemsize > m.itemsize:
                m = x.dtype
        return m

    have_int = len(counts[IntBlock]) > 0
    have_bool = len(counts[BoolBlock]) > 0
    have_object = len(counts[ObjectBlock]) > 0
    have_float = len(counts[FloatBlock]) > 0
    have_complex = len(counts[ComplexBlock]) > 0
    have_dt64 = len(counts[DatetimeBlock]) > 0
    have_td64 = len(counts[TimeDeltaBlock]) > 0
    have_cat = len(counts[CategoricalBlock]) > 0
    have_sparse = len(counts[SparseBlock]) > 0
    have_numeric = have_float or have_complex or have_int

    has_non_numeric = have_dt64 or have_td64 or have_cat

    if (have_object or
        (have_bool and (have_numeric or have_dt64 or have_td64)) or
        (have_numeric and has_non_numeric) or
        have_cat or
        have_dt64 or
        have_td64):
        return np.dtype(object)
    elif have_bool:
        return np.dtype(bool)
    elif have_int and not have_float and not have_complex:

        # if we are mixing unsigned and signed, then return
        # the next biggest int type (if we can)
        lcd = _lcd_dtype(counts[IntBlock])
        kinds = set([i.dtype.kind for i in counts[IntBlock]])
        if len(kinds) == 1:
            return lcd

        if lcd == 'uint64' or lcd == 'int64':
            return np.dtype('int64')

        # return 1 bigger on the itemsize if unsinged
        if lcd.kind == 'u':
            return np.dtype('int%s' % (lcd.itemsize * 8 * 2))
        return lcd

    elif have_complex:
        return np.dtype('c16')
    else:
        return _lcd_dtype(counts[FloatBlock] + counts[SparseBlock])
