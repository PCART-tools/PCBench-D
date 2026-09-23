    def as_matrix(self, columns=None):
        """
        Convert the frame to its Numpy-array matrix representation. Columns
        are presented in sorted order unless a specific list of columns is
        provided.

        NOTE: the dtype will be a lower-common-denominator dtype (implicit
              upcasting) that is to say if the dtypes (even of numeric types)
              are mixed, the one that accommodates all will be chosen use this
              with care if you are not dealing with the blocks

              e.g. if the dtypes are float16,float32         -> float32
                                     float16,float32,float64 -> float64
                                     int32,uint8             -> int32


        Returns
        -------
        values : ndarray
            If the caller is heterogeneous and contains booleans or objects,
            the result will be of dtype=object
        """
        self._consolidate_inplace()
        if self._AXIS_REVERSED:
            return self._data.as_matrix(columns).T
        return self._data.as_matrix(columns)
