    @classmethod
    @Appender(_interval_shared_docs['from_breaks'] % _index_doc_kwargs)
    def from_breaks(cls, breaks, closed='right', name=None, copy=False,
                    dtype=None):
        with rewrite_exception("IntervalArray", cls.__name__):
            array = IntervalArray.from_breaks(breaks, closed=closed, copy=copy,
                                              dtype=dtype)
        return cls._simple_new(array, name=name)
