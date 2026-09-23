    def __contains__(self, key) -> bool:
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
        if not isinstance(key, Interval):
            return False

        try:
            self.get_loc(key)
            return True
        except KeyError:
            return False
