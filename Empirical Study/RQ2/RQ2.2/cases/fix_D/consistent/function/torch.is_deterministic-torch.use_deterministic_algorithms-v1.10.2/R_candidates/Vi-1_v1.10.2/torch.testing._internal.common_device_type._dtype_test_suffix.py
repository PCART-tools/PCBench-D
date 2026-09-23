def _dtype_test_suffix(dtypes):
    """ Returns the test suffix for a dtype, sequence of dtypes, or None. """
    if isinstance(dtypes, list) or isinstance(dtypes, tuple):
        if len(dtypes) == 0:
            return ''
        return '_' + '_'.join((dtype_name(d) for d in dtypes))
    elif dtypes:
        return '_{}'.format(dtype_name(dtypes))
    else:
        return ''
