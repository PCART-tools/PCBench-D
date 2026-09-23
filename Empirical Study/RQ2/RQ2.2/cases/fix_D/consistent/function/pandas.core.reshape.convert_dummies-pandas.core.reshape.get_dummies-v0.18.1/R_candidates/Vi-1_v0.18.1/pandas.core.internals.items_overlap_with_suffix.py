def items_overlap_with_suffix(left, lsuffix, right, rsuffix):
    """
    If two indices overlap, add suffixes to overlapping entries.

    If corresponding suffix is empty, the entry is simply converted to string.

    """
    to_rename = left.intersection(right)
    if len(to_rename) == 0:
        return left, right
    else:
        if not lsuffix and not rsuffix:
            raise ValueError('columns overlap but no suffix specified: %s' %
                             to_rename)

        def lrenamer(x):
            if x in to_rename:
                return '%s%s' % (x, lsuffix)
            return x

        def rrenamer(x):
            if x in to_rename:
                return '%s%s' % (x, rsuffix)
            return x

        return (_transform_index(left, lrenamer),
                _transform_index(right, rrenamer))
