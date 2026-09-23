    def append(self, other):
        """
        Append a collection of Index options together

        Parameters
        ----------
        other : Index or list/tuple of indices

        Returns
        -------
        appended : Index
        """
        to_concat, name = self._ensure_compat_append(other)
        return Index(np.concatenate(to_concat), name=name)
