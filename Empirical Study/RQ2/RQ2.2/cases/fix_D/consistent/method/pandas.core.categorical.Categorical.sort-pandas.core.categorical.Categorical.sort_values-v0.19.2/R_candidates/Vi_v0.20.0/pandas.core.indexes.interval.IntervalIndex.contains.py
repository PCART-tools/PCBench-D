    def contains(self, key):
        """
        return a boolean if this key is IN the index

        We accept / allow keys to be not *just* actual
        objects.

        Parameters
        ----------
        key : int, float, Interval

        Returns
        -------
        boolean
        """
        try:
            self.get_loc(key)
            return True
        except KeyError:
            return False
