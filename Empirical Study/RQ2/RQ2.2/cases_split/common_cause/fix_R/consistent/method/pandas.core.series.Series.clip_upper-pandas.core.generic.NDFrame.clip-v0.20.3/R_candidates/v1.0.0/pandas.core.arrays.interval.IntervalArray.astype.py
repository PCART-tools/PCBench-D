    def astype(self, dtype, copy=True):
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
        dtype = pandas_dtype(dtype)
        if is_interval_dtype(dtype):
            if dtype == self.dtype:
                return self.copy() if copy else self

            # need to cast to different subtype
            try:
                new_left = self.left.astype(dtype.subtype)
                new_right = self.right.astype(dtype.subtype)
            except TypeError:
                msg = (
                    f"Cannot convert {self.dtype} to {dtype}; subtypes are incompatible"
                )
                raise TypeError(msg)
            return self._shallow_copy(new_left, new_right)
        elif is_categorical_dtype(dtype):
            return Categorical(np.asarray(self))
        # TODO: This try/except will be repeated.
        try:
            return np.asarray(self).astype(dtype, copy=copy)
        except (TypeError, ValueError):
            msg = f"Cannot cast {type(self).__name__} to dtype {dtype}"
            raise TypeError(msg)
