    def as_array(
        self,
        dtype: np.dtype | None = None,
        copy: bool = False,
        na_value: object = lib.no_default,
    ) -> np.ndarray:
        """
        Convert the blockmanager data into an numpy array.

        Parameters
        ----------
        dtype : np.dtype or None, default None
            Data type of the return array.
        copy : bool, default False
            If True then guarantee that a copy is returned. A value of
            False does not guarantee that the underlying data is not
            copied.
        na_value : object, default lib.no_default
            Value to be used as the missing value sentinel.

        Returns
        -------
        arr : ndarray
        """
        # TODO(CoW) handle case where resulting array is a view
        if len(self.blocks) == 0:
            arr = np.empty(self.shape, dtype=float)
            return arr.transpose()

        # We want to copy when na_value is provided to avoid
        # mutating the original object
        copy = copy or na_value is not lib.no_default

        if self.is_single_block:
            blk = self.blocks[0]
            if blk.is_extension:
                # Avoid implicit conversion of extension blocks to object

                # error: Item "ndarray" of "Union[ndarray, ExtensionArray]" has no
                # attribute "to_numpy"
                arr = blk.values.to_numpy(  # type: ignore[union-attr]
                    dtype=dtype,
                    na_value=na_value,
                ).reshape(blk.shape)
            else:
                arr = np.asarray(blk.get_values())
                if dtype:
                    arr = arr.astype(dtype, copy=False)
        else:
            arr = self._interleave(dtype=dtype, na_value=na_value)
            # The underlying data was copied within _interleave
            copy = False

        if copy:
            arr = arr.copy()

        if na_value is not lib.no_default:
            arr[isna(arr)] = na_value

        return arr.transpose()
