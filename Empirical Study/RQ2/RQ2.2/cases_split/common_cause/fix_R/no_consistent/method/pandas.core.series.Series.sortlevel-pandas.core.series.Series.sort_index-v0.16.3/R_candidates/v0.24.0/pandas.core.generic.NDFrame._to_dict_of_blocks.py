    def _to_dict_of_blocks(self, copy=True):
        """
        Return a dict of dtype -> Constructor Types that
        each is a homogeneous dtype.

        Internal ONLY
        """
        return {k: self._constructor(v).__finalize__(self)
                for k, v, in self._data.to_dict(copy=copy).items()}
