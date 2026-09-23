def _interpolate_scipy_wrapper(x, y, new_x, method, fill_value=None,
                               bounds_error=False, order=None):
    """
    passed off to scipy.interpolate.interp1d. method is scipy's kind.
    Returns an array interpolated at new_x.  Add any new methods to
    the list in _clean_interp_method
    """
    try:
        from scipy import interpolate
        from pandas import DatetimeIndex
    except ImportError:
        raise ImportError('{0} interpolation requires Scipy'.format(method))

    new_x = np.asarray(new_x)

    # ignores some kwargs that could be passed along.
    alt_methods = {
        'barycentric': interpolate.barycentric_interpolate,
        'krogh': interpolate.krogh_interpolate,
        'piecewise_polynomial': interpolate.piecewise_polynomial_interpolate,
    }

    if getattr(x, 'is_all_dates', False):
        # GH 5975, scipy.interp1d can't hande datetime64s
        x, new_x = x.values.astype('i8'), new_x.astype('i8')

    try:
        alt_methods['pchip'] = interpolate.pchip_interpolate
    except AttributeError:
        if method == 'pchip':
            raise ImportError("Your version of scipy does not support "
                              "PCHIP interpolation.")

    interp1d_methods = ['nearest', 'zero', 'slinear', 'quadratic', 'cubic',
                        'polynomial']
    if method in interp1d_methods:
        if method == 'polynomial':
            method = order
        terp = interpolate.interp1d(x, y, kind=method, fill_value=fill_value,
                                    bounds_error=bounds_error)
        new_y = terp(new_x)
    elif method == 'spline':
        terp = interpolate.UnivariateSpline(x, y, k=order)
        new_y = terp(new_x)
    else:
        # GH 7295: need to be able to write for some reason
        # in some circumstances: check all three
        if not x.flags.writeable:
            x = x.copy()
        if not y.flags.writeable:
            y = y.copy()
        if not new_x.flags.writeable:
            new_x = new_x.copy()
        method = alt_methods[method]
        new_y = method(x, y, new_x)
    return new_y
