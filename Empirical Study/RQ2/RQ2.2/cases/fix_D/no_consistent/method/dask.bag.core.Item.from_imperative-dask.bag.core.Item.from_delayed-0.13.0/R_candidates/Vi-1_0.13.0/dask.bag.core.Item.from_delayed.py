    @staticmethod
    def from_delayed(value):
        """ Create bag item from a dask.delayed value

        See ``dask.bag.from_delayed`` for details
        """
        from dask.delayed import Delayed
        assert isinstance(value, Delayed)
        return Item(value.dask, value.key)
