    def append(self, other):
        """
        Append a collection of CategoricalIndex options together

        Parameters
        ----------
        other : Index or list/tuple of indices

        Returns
        -------
        appended : Index

        Raises
        ------
        ValueError if other is not in the categories
        """
        to_concat, name = self._ensure_compat_append(other)
        to_concat = [ self._is_dtype_compat(c) for c in to_concat ]
        codes = np.concatenate([ c.codes for c in to_concat ])
        return self._create_from_codes(codes, name=name)
