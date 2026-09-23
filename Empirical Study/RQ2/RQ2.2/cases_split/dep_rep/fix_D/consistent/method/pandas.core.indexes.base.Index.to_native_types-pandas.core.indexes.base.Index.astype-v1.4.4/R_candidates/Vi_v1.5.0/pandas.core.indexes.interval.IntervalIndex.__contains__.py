    def __contains__(self, key: Any) -> bool:
        """
        return a boolean if this key is IN the index
        We *only* accept an Interval

        Parameters
        ----------
        key : Interval

        Returns
        -------
        bool
        """
        hash(key)
        if not isinstance(key, Interval):
            if is_valid_na_for_dtype(key, self.dtype):
                return self.hasnans
            return False

        try:
            self.get_loc(key)
            return True
        except KeyError:
            return False
