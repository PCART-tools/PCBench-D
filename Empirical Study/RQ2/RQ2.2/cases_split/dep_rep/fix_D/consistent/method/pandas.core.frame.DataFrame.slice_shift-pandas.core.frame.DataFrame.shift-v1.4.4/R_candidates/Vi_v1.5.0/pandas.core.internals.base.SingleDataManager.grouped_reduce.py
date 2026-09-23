    def grouped_reduce(self, func, ignore_failures: bool = False):
        """
        ignore_failures : bool, default False
            Not used; for compatibility with ArrayManager/BlockManager.
        """

        arr = self.array
        res = func(arr)
        index = default_index(len(res))

        mgr = type(self).from_array(res, index)
        return mgr
