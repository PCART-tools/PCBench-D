
    def take(self, indices, axis=0, convert=True):
        """
        Analogous to ndarray.take, return DataFrame corresponding to requested
        indices along an axis

        Parameters
        ----------
        indices : list / array of ints
        axis : {0, 1}
        convert : convert indices for negative values, check bounds, default True
                  mainly useful for an user routine calling

        Returns
        -------
        taken : DataFrame
        """

        # check/convert indicies here
        if convert:
            axis = self._get_axis_number(axis)
            indices = _maybe_convert_indices(indices, len(self._get_axis(axis)))

        if self._is_mixed_type:
            if axis == 0:
                new_data = self._data.take(indices, axis=1, verify=False)
                return DataFrame(new_data)
            else:
                new_columns = self.columns.take(indices)
                return self.reindex(columns=new_columns)
        else:
            new_values = com.take_nd(self.values,
                                     com._ensure_int64(indices),
                                     axis=axis)
            if axis == 0:
                new_columns = self.columns
                new_index = self.index.take(indices)
            else:
                new_columns = self.columns.take(indices)
                new_index = self.index
            return DataFrame(new_values, index=new_index,
                             columns=new_columns)
