    def astype(self, dtype, copy: bool = True):
        """
        Cast to an ExtensionArray or NumPy array with dtype 'dtype'.

        Parameters
        ----------
        dtype : str or dtype
            Typecode or data-type to which the array is cast.

        copy : bool, default True
            Whether to copy the data, even if not necessary. If False,
            a copy is made only if the old dtype does not match the
            new dtype.

        Returns
        -------
        array : ExtensionArray or ndarray
            ExtensionArray or NumPy ndarray with 'dtype' for its dtype.
        """
        from pandas import Index

        if dtype is not None:
            dtype = pandas_dtype(dtype)

        if isinstance(dtype, IntervalDtype):
            if dtype == self.dtype:
                return self.copy() if copy else self

            if is_float_dtype(self.dtype.subtype) and needs_i8_conversion(
                dtype.subtype
            ):
                # This is allowed on the Index.astype but we disallow it here
                msg = (
                    f"Cannot convert {self.dtype} to {dtype}; subtypes are incompatible"
                )
                raise TypeError(msg)

            # need to cast to different subtype
            try:
                # We need to use Index rules for astype to prevent casting
                #  np.nan entries to int subtypes
                new_left = Index(self._left, copy=False).astype(dtype.subtype)
                new_right = Index(self._right, copy=False).astype(dtype.subtype)
            except IntCastingNaNError:
                # e.g test_subtype_integer
                raise
            except (TypeError, ValueError) as err:
                # e.g. test_subtype_integer_errors f8->u8 can be lossy
                #  and raises ValueError
                msg = (
                    f"Cannot convert {self.dtype} to {dtype}; subtypes are incompatible"
                )
                raise TypeError(msg) from err
            return self._shallow_copy(new_left, new_right)
        else:
            try:
                return super().astype(dtype, copy=copy)
            except (TypeError, ValueError) as err:
                msg = f"Cannot cast {type(self).__name__} to dtype {dtype}"
                raise TypeError(msg) from err
