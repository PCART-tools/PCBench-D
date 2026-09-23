    def take(self, indices, axis=0, convert=True, is_copy=False, **kwargs):
        """
        return Series corresponding to requested indices

        Parameters
        ----------
        indices : list / array of ints
        convert : translate negative to positive indices (default)

        Returns
        -------
        taken : Series

        See also
        --------
        numpy.ndarray.take
        """
        if kwargs:
            nv.validate_take(tuple(), kwargs)

        # check/convert indicies here
        if convert:
            indices = maybe_convert_indices(indices, len(self._get_axis(axis)))

        indices = _ensure_platform_int(indices)
        new_index = self.index.take(indices)
        new_values = self._values.take(indices)
        return (self._constructor(new_values, index=new_index, fastpath=True)
                    .__finalize__(self))
