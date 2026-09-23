    @classmethod
    @Appender(_interval_shared_docs["from_intervals"] % _index_doc_kwargs)
    def from_intervals(cls, data, closed=None, name=None, copy=False, dtype=None):
        msg = (
            "IntervalIndex.from_intervals is deprecated and will be "
            "removed in a future version; Use IntervalIndex(...) instead"
        )
        warnings.warn(msg, FutureWarning, stacklevel=2)
        with rewrite_exception("IntervalArray", cls.__name__):
            array = IntervalArray(data, closed=closed, copy=copy, dtype=dtype)

        if name is None and isinstance(data, cls):
            name = data.name

        return cls._simple_new(array, name=name)
