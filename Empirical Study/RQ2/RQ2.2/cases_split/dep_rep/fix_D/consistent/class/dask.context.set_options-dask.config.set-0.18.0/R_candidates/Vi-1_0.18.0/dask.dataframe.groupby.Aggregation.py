class Aggregation(object):
    """A user defined aggregation.

    Parameters
    ----------
    name : str
        the name of the aggregation. It should be unique, since intermediate
        result will be identified by this name.
    chunk : callable
        a function that will be called with the grouped column of each
        partition. It can either return a single series or a tuple of series.
        The index has to be equal to the groups.
    agg : callable
        a function that will be called to aggregate the results of each chunk.
        Again the argument(s) will be grouped series. If ``chunk`` returned a
        tuple, ``agg`` will be called with all of them as individual positional
        arguments.
    finalize : callable
        an optional finalizer that will be called with the results from the
        aggregation.

    Examples
    --------

    ``sum`` can be implemented as::

        custom_sum = dd.Aggregation('custom_sum', lambda s: s.sum(), lambda s0: s0.sum())
        df.groupby('g').agg(custom_sum)

    and ``mean`` can be implemented as::

        custom_mean = dd.Aggregation(
            'custom_mean',
            lambda s: (s.count(), s.sum()),
            lambda count, sum: (count.sum(), sum.sum()),
            lambda count, sum: sum / count,
        )
        df.groupby('g').agg(custom_mean)

    """
    def __init__(self, name, chunk, agg, finalize=None):
        self.chunk = chunk
        self.agg = agg
        self.finalize = finalize
        self.__name__ = name
