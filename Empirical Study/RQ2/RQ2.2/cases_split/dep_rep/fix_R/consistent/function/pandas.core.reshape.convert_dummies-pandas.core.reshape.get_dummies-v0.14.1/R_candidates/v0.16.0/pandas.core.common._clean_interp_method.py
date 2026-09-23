def _clean_interp_method(method, order=None):
    valid = ['linear', 'time', 'index', 'values', 'nearest', 'zero', 'slinear',
             'quadratic', 'cubic', 'barycentric', 'polynomial',
             'krogh', 'piecewise_polynomial',
             'pchip', 'spline']
    if method in ('spline', 'polynomial') and order is None:
        raise ValueError("You must specify the order of the spline or "
                         "polynomial.")
    if method not in valid:
        raise ValueError("method must be one of {0}."
                         "Got '{1}' instead.".format(valid, method))
    return method
