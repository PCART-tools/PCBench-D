def _select_function(sort, typ):
    if typ in ['F','D']:
        if callable(sort):
            # assume the user knows what they're doing
            sfunction = sort
        elif sort == 'lhp':
            sfunction = lambda x,y: (np.real(x/y) < 0.0)
        elif sort == 'rhp':
            sfunction = lambda x,y: (np.real(x/y) >= 0.0)
        elif sort == 'iuc':
            sfunction = lambda x,y: (abs(x/y) <= 1.0)
        elif sort == 'ouc':
            sfunction = lambda x,y: (abs(x/y) > 1.0)
        else:
            raise ValueError("sort parameter must be None, a callable, or "
                "one of ('lhp','rhp','iuc','ouc')")
    elif typ in ['f','d']:
        if callable(sort):
            # assume the user knows what they're doing
            sfunction = sort
        elif sort == 'lhp':
            sfunction = lambda x,y,z: (np.real((x+y*1j)/z) < 0.0)
        elif sort == 'rhp':
            sfunction = lambda x,y,z: (np.real((x+y*1j)/z) >= 0.0)
        elif sort == 'iuc':
            sfunction = lambda x,y,z: (abs((x+y*1j)/z) <= 1.0)
        elif sort == 'ouc':
            sfunction = lambda x,y,z: (abs((x+y*1j)/z) > 1.0)
        else:
            raise ValueError("sort parameter must be None, a callable, or "
                "one of ('lhp','rhp','iuc','ouc')")
    else:  # to avoid an error later
        raise ValueError("dtype %s not understood" % typ)
    return sfunction
