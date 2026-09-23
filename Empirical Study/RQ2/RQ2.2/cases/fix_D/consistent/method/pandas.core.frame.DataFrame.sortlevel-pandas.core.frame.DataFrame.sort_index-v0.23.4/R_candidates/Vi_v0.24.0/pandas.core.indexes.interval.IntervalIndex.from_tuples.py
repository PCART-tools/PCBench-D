    @classmethod
    @Appender(_interval_shared_docs['from_tuples'] % _index_doc_kwargs)
    def from_tuples(cls, data, closed='right', name=None, copy=False,
                    dtype=None):
        with rewrite_exception("IntervalArray", cls.__name__):
            arr = IntervalArray.from_tuples(data, closed=closed, copy=copy,
                                            dtype=dtype)
        return cls._simple_new(arr, name=name)
