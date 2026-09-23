    def as_matrix(self, columns=None):
        """
        Convert the frame to its Numpy-array representation.

        Parameters
        ----------
        columns: list, optional, default:None
            If None, return all columns, otherwise, returns specified columns.

        Returns
        -------
        values : ndarray
            If the caller is heterogeneous and contains booleans or objects,
            the result will be of dtype=object. See Notes.


        Notes
        -----
        Return is NOT a Numpy-matrix, rather, a Numpy-array.

        The dtype will be a lower-common-denominator dtype (implicit
        upcasting); that is to say if the dtypes (even of numeric types)
        are mixed, the one that accommodates all will be chosen. Use this
        with care if you are not dealing with the blocks.

        e.g. If the dtypes are float16 and float32, dtype will be upcast to
        float32.  If dtypes are int32 and uint8, dtype will be upcase to
        int32. By numpy.find_common_type convention, mixing int64 and uint64
        will result in a flot64 dtype.

        This method is provided for backwards compatibility. Generally,
        it is recommended to use '.values'.

        See Also
        --------
        pandas.DataFrame.values
        """
        self._consolidate_inplace()
        if self._AXIS_REVERSED:
            return self._data.as_matrix(columns).T
        return self._data.as_matrix(columns)
