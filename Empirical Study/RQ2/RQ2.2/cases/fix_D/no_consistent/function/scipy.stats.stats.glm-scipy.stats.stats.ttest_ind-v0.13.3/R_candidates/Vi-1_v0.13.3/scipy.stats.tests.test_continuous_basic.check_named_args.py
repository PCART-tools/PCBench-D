def check_named_args(distfn, x, shape_args, defaults, meths):
    """Check calling w/ named arguments."""

    # check consistency of shapes, numargs and _parse signature
    signature = inspect.getargspec(distfn._parse_args)
    npt.assert_(signature.varargs is None)
    npt.assert_(signature.keywords is None)
    npt.assert_(signature.defaults == defaults)

    shape_argnames = signature.args[1:-len(defaults)]  # self, a, b, loc=0, scale=1
    if distfn.shapes:
        shapes_ = distfn.shapes.replace(',',' ').split()
    else:
        shapes_ = ''
    npt.assert_(len(shapes_) == distfn.numargs)
    npt.assert_(len(shapes_) == len(shape_argnames))

    # check calling w/ named arguments
    shape_args = list(shape_args)

    vals = [meth(x, *shape_args) for meth in meths]
    npt.assert_(np.all(np.isfinite(vals)))

    names, a, k = shape_argnames[:], shape_args[:], {}
    while names:
        k.update({names.pop(): a.pop()})
        v = [meth(x, *a, **k) for meth in meths]
        npt.assert_array_equal(vals, v)
        if not 'n' in k.keys():
            # `n` is first parameter of moment(), so can't be used as named arg
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                npt.assert_equal(distfn.moment(3, *a, **k),
                                 distfn.moment(3, *shape_args))

    # unknown arguments should not go through:
    k.update({'kaboom': 42})
    npt.assert_raises(TypeError, distfn.cdf, x, **k)
