    @staticmethod
    def from_delayed(value):
        """ Create bag item from a dask.delayed value

        See ``dask.bag.from_delayed`` for details
        """
        from dask.delayed import Delayed, delayed
        if not isinstance(value, Delayed) and hasattr(value, 'key'):
            value = delayed(value)
        assert isinstance(value, Delayed)
        return Item(ensure_dict(value.dask), value.key)
