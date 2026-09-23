def _concat_datetimetz(to_concat, name=None):
    """
    concat DatetimeIndex with the same tz
    all inputs must be DatetimeIndex
    it is used in DatetimeIndex.append also
    """
    # Right now, internals will pass a List[DatetimeArray] here
    # for reductions like quantile. I would like to disentangle
    # all this before we get here.
    sample = to_concat[0]

    if isinstance(sample, ABCIndexClass):
        return sample._concat_same_dtype(to_concat, name=name)
    elif isinstance(sample, ABCDatetimeArray):
        return sample._concat_same_type(to_concat)
