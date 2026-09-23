def interpolate_1d(xvalues, yvalues, method='linear', limit=None,
                   limit_direction='forward', fill_value=None,
                   bounds_error=False, order=None, **kwargs):
    """
    Logic for the 1-d interpolation.  The result should be 1-d, inputs
    xvalues and yvalues will each be 1-d arrays of the same length.

    Bounds_error is currently hardcoded to False since non-scipy ones don't
    take it as an argumnet.
    """
    # Treat the original, non-scipy methods first.

    invalid = isnull(yvalues)
    valid = ~invalid

    if not valid.any():
        # have to call np.asarray(xvalues) since xvalues could be an Index
        # which cant be mutated
        result = np.empty_like(np.asarray(xvalues), dtype=np.float64)
        result.fill(np.nan)
        return result

    if valid.all():
        return yvalues

    if method == 'time':
        if not getattr(xvalues, 'is_all_dates', None):
            # if not issubclass(xvalues.dtype.type, np.datetime64):
            raise ValueError('time-weighted interpolation only works '
                             'on Series or DataFrames with a '
                             'DatetimeIndex')
        method = 'values'

    def _interp_limit(invalid, fw_limit, bw_limit):
        "Get idx of values that won't be filled b/c they exceed the limits."
        for x in np.where(invalid)[0]:
            if invalid[max(0, x - fw_limit):x + bw_limit + 1].all():
                yield x

    valid_limit_directions = ['forward', 'backward', 'both']
    limit_direction = limit_direction.lower()
    if limit_direction not in valid_limit_directions:
        raise ValueError('Invalid limit_direction: expecting one of %r, got '
                         '%r.' % (valid_limit_directions, limit_direction))

    from pandas import Series
    ys = Series(yvalues)
    start_nans = set(range(ys.first_valid_index()))
    end_nans = set(range(1 + ys.last_valid_index(), len(valid)))

    # This is a list of the indexes in the series whose yvalue is currently
    # NaN, but whose interpolated yvalue will be overwritten with NaN after
    # computing the interpolation. For each index in this list, one of these
    # conditions is true of the corresponding NaN in the yvalues:
    #
    # a) It is one of a chain of NaNs at the beginning of the series, and
    #    either limit is not specified or limit_direction is 'forward'.
    # b) It is one of a chain of NaNs at the end of the series, and limit is
    #    specified and limit_direction is 'backward' or 'both'.
    # c) Limit is nonzero and it is further than limit from the nearest non-NaN
    #    value (with respect to the limit_direction setting).
    #
    # The default behavior is to fill forward with no limit, ignoring NaNs at
    # the beginning (see issues #9218 and #10420)
    violate_limit = sorted(start_nans)

    if limit:
        if limit_direction == 'forward':
            violate_limit = sorted(start_nans | set(_interp_limit(invalid,
                                                                  limit, 0)))
        if limit_direction == 'backward':
            violate_limit = sorted(end_nans | set(_interp_limit(invalid, 0,
                                                                limit)))
        if limit_direction == 'both':
            violate_limit = sorted(_interp_limit(invalid, limit, limit))

    xvalues = getattr(xvalues, 'values', xvalues)
    yvalues = getattr(yvalues, 'values', yvalues)
    result = yvalues.copy()

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
        result[invalid] = np.interp(inds[invalid], inds[valid], yvalues[valid])
        result[violate_limit] = np.nan
        return result

    sp_methods = ['nearest', 'zero', 'slinear', 'quadratic', 'cubic',
                  'barycentric', 'krogh', 'spline', 'polynomial',
                  'from_derivatives', 'piecewise_polynomial', 'pchip', 'akima']

    if method in sp_methods:
        inds = np.asarray(xvalues)
        # hack for DatetimeIndex, #1646
        if issubclass(inds.dtype.type, np.datetime64):
            inds = inds.view(np.int64)
        result[invalid] = _interpolate_scipy_wrapper(inds[valid],
                                                     yvalues[valid],
                                                     inds[invalid],
                                                     method=method,
                                                     fill_value=fill_value,
                                                     bounds_error=bounds_error,
                                                     order=order, **kwargs)
        result[violate_limit] = np.nan
        return result
