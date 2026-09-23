def _validate_join_method(method):
    if method not in ['left', 'right', 'inner', 'outer']:
        raise ValueError('do not recognize join method %s' % method)
