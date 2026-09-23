def is_datetimetz(array):
    """ return if we are a datetime with tz array """
    return ((isinstance(array, gt.ABCDatetimeIndex) and
             getattr(array, 'tz', None) is not None) or
            is_datetime64tz_dtype(array))
