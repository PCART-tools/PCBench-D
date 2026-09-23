    def _is_valid_list_like(self, key, axis):
        # return a boolean if we are a valid list-like (e.g. that we don't
        # have out-of-bounds values)

        # a tuple should already have been caught by this point
        # so don't treat a tuple as a valid indexer
        if isinstance(key, tuple):
            raise IndexingError('Too many indexers')

        # coerce the key to not exceed the maximum size of the index
        arr = np.array(key)
        ax = self.obj._get_axis(axis)
        l = len(ax)
        if (hasattr(arr, '__len__') and len(arr) and
                (arr.max() >= l or arr.min() < -l)):
            raise IndexError("positional indexers are out-of-bounds")

        return True
