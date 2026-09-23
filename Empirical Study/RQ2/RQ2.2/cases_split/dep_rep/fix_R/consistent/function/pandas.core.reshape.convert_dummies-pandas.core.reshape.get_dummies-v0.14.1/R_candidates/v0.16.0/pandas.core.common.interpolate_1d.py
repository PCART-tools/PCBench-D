def interpolate_1d(xvalues, yvalues, method='linear', limit=None,
                   fill_value=None, bounds_error=False, order=None):
    """
    Logic for the 1-d interpolation.  The result should be 1-d, inputs
    xvalues and yvalues will each be 1-d arrays of the same length.

    Bounds_error is currently hardcoded to False since non-scipy ones don't
    take it as an argumnet.
    """
    # Treat the original, non-scipy methods first.

    invalid = isnull(yvalues)
    valid = ~invalid

    valid_y = yvalues[valid]
    valid_x = xvalues[valid]
    new_x = xvalues[invalid]

    if method == 'time':
        if not getattr(xvalues, 'is_all_dates', None):
        # if not issubclass(xvalues.dtype.type, np.datetime64):
            raise ValueError('time-weighted interpolation only works '
                             'on Series or DataFrames with a '
                             'DatetimeIndex')
        method = 'values'

    def _interp_limit(invalid, limit):
        """mask off values that won't be filled since they exceed the limit"""
        all_nans = np.where(invalid)[0]
        if all_nans.size == 0: # no nans anyway
            return []
        violate = [invalid[x:x + limit + 1] for x in all_nans]
        violate = np.array([x.all() & (x.size > limit) for x in violate])
        return all_nans[violate] + limit

    xvalues = getattr(xvalues, 'values', xvalues)
    yvalues = getattr(yvalues, 'values', yvalues)

    if limit:
        violate_limit = _interp_limit(invalid, limit)
    if valid.any():
        firstIndex = valid.argmax()
        valid = valid[firstIndex:]
        invalid = invalid[firstIndex:]
        result = yvalues.copy()
        if valid.all():
            return yvalues
    else:
        # have to call np.array(xvalues) since xvalues could be an Index
        # which cant be mutated
        result = np.empty_like(np.array(xvalues), dtype=np.float64)
        result.fill(np.nan)
        return result

    if method in ['linear', 'time', 'index', 'values']:
        if method in ('values', 'index'):
            inds = np.asarray(xvalues)
            # hack for DatetimeIndex, #1646
            if issubclass(inds.dtype.type, np.datetime64):
                inds = inds.view(np.int64)

            if inds.dtype == np.object_:
                inds = lib.maybe_convert_objects(inds)
        else:
            inds = xvalues

        inds = inds[firstIndex:]

        result[firstIndex:][invalid] = np.interp(inds[invalid], inds[valid],
                                                 yvalues[firstIndex:][valid])

        if limit:
            result[violate_limit] = np.nan
        return result

    sp_methods = ['nearest', 'zero', 'slinear', 'quadratic', 'cubic',
                  'barycentric', 'krogh', 'spline', 'polynomial',
                  'piecewise_polynomial', 'pchip']
    if method in sp_methods:
        new_x = new_x[firstIndex:]
        xvalues = xvalues[firstIndex:]

        result[firstIndex:][invalid] = _interpolate_scipy_wrapper(
            valid_x, valid_y, new_x, method=method, fill_value=fill_value,
            bounds_error=bounds_error, order=order)
        if limit:
            result[violate_limit] = np.nan
        return result
