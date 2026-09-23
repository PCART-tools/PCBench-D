def _doc_parms(cls):
    """Return a tuple of the doc parms."""
    axis_descr = "{%s}" % ', '.join(["{0} ({1})".format(a, i)
                                     for i, a in enumerate(cls._AXIS_ORDERS)])
    name = (cls._constructor_sliced.__name__
            if cls._AXIS_LEN > 1 else 'scalar')
    name2 = cls.__name__
    return axis_descr, name, name2
