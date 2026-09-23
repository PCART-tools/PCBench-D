    def _ixs(self, i, axis=0, copy=False):
        """
        i : int, slice, or sequence of integers
        axis : int
        """

        # irow
        if axis == 0:

            """
            Notes
            -----
            If slice passed, the resulting data will be a view
            """

            if isinstance(i, slice):
                return self[i]
            else:
                label = self.index[i]
                if isinstance(label, Index):

                    # a location index by definition
                    i = _maybe_convert_indices(i, len(self._get_axis(axis)))
                    result = self.reindex(i, takeable=True)
                    copy=True
                else:
                    new_values, copy = self._data.fast_2d_xs(i, copy=copy)
                    result = Series(new_values, index=self.columns,
                                    name=self.index[i], dtype=new_values.dtype)
                result._set_is_copy(self, copy=copy)
                return result

        # icol
        else:

            """
            Notes
            -----
            If slice passed, the resulting data will be a view
            """

            label = self.columns[i]
            if isinstance(i, slice):
                # need to return view
                lab_slice = slice(label[0], label[-1])
                return self.ix[:, lab_slice]
            else:
                label = self.columns[i]
                if isinstance(label, Index):
                    return self.take(i, axis=1, convert=True)

                # if the values returned are not the same length
                # as the index (iow a not found value), iget returns
                # a 0-len ndarray. This is effectively catching
                # a numpy error (as numpy should really raise)
                values = self._data.iget(i)
                if not len(values):
                    values = np.array([np.nan] * len(self.index), dtype=object)
                result = self._constructor_sliced.from_array(
                    values, index=self.index,
                    name=label, fastpath=True)

                # this is a cached value, mark it so
                result._set_as_cached(i, self)

                return result
