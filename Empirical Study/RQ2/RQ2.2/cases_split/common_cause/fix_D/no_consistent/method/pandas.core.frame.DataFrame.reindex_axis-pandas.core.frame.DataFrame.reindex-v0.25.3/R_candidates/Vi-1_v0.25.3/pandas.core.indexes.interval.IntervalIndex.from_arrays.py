    @classmethod
    @Appender(_interval_shared_docs["from_arrays"] % _index_doc_kwargs)
    def from_arrays(
        cls, left, right, closed="right", name=None, copy=False, dtype=None
    ):
        with rewrite_exception("IntervalArray", cls.__name__):
            array = IntervalArray.from_arrays(
                left, right, closed, copy=copy, dtype=dtype
            )
        return cls._simple_new(array, name=name)
