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
                    "Cannot convert {dtype} to {new_dtype}; subtypes are "
                    "incompatible"
                )
                raise TypeError(msg.format(dtype=self.dtype, new_dtype=dtype))
            return self._shallow_copy(new_left, new_right)
        elif is_categorical_dtype(dtype):
            return Categorical(np.asarray(self))
        # TODO: This try/except will be repeated.
        try:
            return np.asarray(self).astype(dtype, copy=copy)
        except (TypeError, ValueError):
            msg = "Cannot cast {name} to dtype {dtype}"
            raise TypeError(msg.format(name=type(self).__name__, dtype=dtype))
