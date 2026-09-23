    def take(self, indices, axis=0, convert=True):
        """
        Analogous to ndarray.take, return Series corresponding to requested
        indices

        Parameters
        ----------
        indices : list / array of ints
        convert : translate negative to positive indices (default)

        Returns
        -------
        taken : Series
        """
        # check/convert indicies here
        if convert:
            indices = _maybe_convert_indices(
                indices, len(self._get_axis(axis)))

        indices = com._ensure_platform_int(indices)
        new_index = self.index.take(indices)
        new_values = self.values.take(indices)
        return self._constructor(new_values,
                                 index=new_index).__finalize__(self)
