def _create_methods(arith_method, radd_func, comp_method, bool_method,
                    use_numexpr, special=False, default_axis='columns'):
    # creates actual methods based upon arithmetic, comp and bool method
    # constructors.

    # NOTE: Only frame cares about default_axis, specifically: special methods
    # have default axis None, whereas flex methods have default axis 'columns'
    # if we're not using numexpr, then don't pass a str_rep
    if use_numexpr:
        op = lambda x: x
    else:
        op = lambda x: None
    if special:
        def names(x):
            if x[-1] == "_":
                return "__%s_" % x
            else:
                return "__%s__" % x
    else:
        names = lambda x: x
    radd_func = radd_func or operator.add
    # Inframe, all special methods have default_axis=None, flex methods have
    # default_axis set to the default (columns)
    new_methods = dict(
        add=arith_method(operator.add, names('add'), op('+'),
                         default_axis=default_axis),
        radd=arith_method(radd_func, names('radd'), op('+'),
                          default_axis=default_axis),
        sub=arith_method(operator.sub, names('sub'), op('-'),
                         default_axis=default_axis),
        mul=arith_method(operator.mul, names('mul'), op('*'),
                         default_axis=default_axis),
        truediv=arith_method(operator.truediv, names('truediv'), op('/'),
                             truediv=True, fill_zeros=np.inf,
                             default_axis=default_axis),
        floordiv=arith_method(operator.floordiv, names('floordiv'), op('//'),
                              default_axis=default_axis, fill_zeros=np.inf),
        # Causes a floating point exception in the tests when numexpr
        # enabled, so for now no speedup
        mod=arith_method(operator.mod, names('mod'), None,
                         default_axis=default_axis, fill_zeros=np.nan),
        pow=arith_method(operator.pow, names('pow'), op('**'),
                         default_axis=default_axis),
        # not entirely sure why this is necessary, but previously was included
        # so it's here to maintain compatibility
        rmul=arith_method(operator.mul, names('rmul'), op('*'),
                          default_axis=default_axis, reversed=True),
        rsub=arith_method(lambda x, y: y - x, names('rsub'), op('-'),
                          default_axis=default_axis, reversed=True),
        rtruediv=arith_method(lambda x, y: operator.truediv(y, x),
                              names('rtruediv'), op('/'), truediv=True,
                              fill_zeros=np.inf, default_axis=default_axis,
                              reversed=True),
        rfloordiv=arith_method(lambda x, y: operator.floordiv(y, x),
                               names('rfloordiv'), op('//'),
                               default_axis=default_axis, fill_zeros=np.inf,
                               reversed=True),
        rpow=arith_method(lambda x, y: y ** x, names('rpow'), op('**'),
                          default_axis=default_axis, reversed=True),
        rmod=arith_method(lambda x, y: y % x, names('rmod'), op('%'),
                          default_axis=default_axis, fill_zeros=np.nan,
                          reversed=True),
    )
    new_methods['div'] = new_methods['truediv']
    new_methods['rdiv'] = new_methods['rtruediv']

    # Comp methods never had a default axis set
    if comp_method:
        new_methods.update(dict(
            eq=comp_method(operator.eq, names('eq'), op('==')),
            ne=comp_method(operator.ne, names('ne'), op('!='), masker=True),
            lt=comp_method(operator.lt, names('lt'), op('<')),
            gt=comp_method(operator.gt, names('gt'), op('>')),
            le=comp_method(operator.le, names('le'), op('<=')),
            ge=comp_method(operator.ge, names('ge'), op('>=')),
        ))
    if bool_method:
        new_methods.update(dict(
            and_=bool_method(operator.and_, names('and_'), op('&')),
            or_=bool_method(operator.or_, names('or_'), op('|')),
            # For some reason ``^`` wasn't used in original.
            xor=bool_method(operator.xor, names('xor'), op('^')),
            rand_=bool_method(lambda x, y: operator.and_(y, x),
                              names('rand_'), op('&')),
            ror_=bool_method(lambda x, y: operator.or_(y, x), names('ror_'), op('|')),
            rxor=bool_method(lambda x, y: operator.xor(y, x), names('rxor'), op('^'))
        ))

    new_methods = dict((names(k), v) for k, v in new_methods.items())
    return new_methods
