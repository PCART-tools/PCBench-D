def _clean_fill_method(method, allow_nearest=False):
    if method is None:
        return None
    method = method.lower()
    if method == 'ffill':
        method = 'pad'
    if method == 'bfill':
        method = 'backfill'

    valid_methods = ['pad', 'backfill']
    expecting = 'pad (ffill) or backfill (bfill)'
    if allow_nearest:
        valid_methods.append('nearest')
        expecting = 'pad (ffill), backfill (bfill) or nearest'
    if method not in valid_methods:
        msg = ('Invalid fill method. Expecting %s. Got %s'
               % (expecting, method))
        raise ValueError(msg)
    return method
