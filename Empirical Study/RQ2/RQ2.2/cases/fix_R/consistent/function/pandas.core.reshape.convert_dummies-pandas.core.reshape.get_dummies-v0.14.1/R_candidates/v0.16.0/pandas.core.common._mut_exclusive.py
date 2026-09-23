def _mut_exclusive(**kwargs):
    item1, item2 = kwargs.items()
    label1, val1 = item1
    label2, val2 = item2
    if val1 is not None and val2 is not None:
        raise TypeError('mutually exclusive arguments: %r and %r' %
                        (label1, label2))
    elif val1 is not None:
        return val1
    else:
        return val2
