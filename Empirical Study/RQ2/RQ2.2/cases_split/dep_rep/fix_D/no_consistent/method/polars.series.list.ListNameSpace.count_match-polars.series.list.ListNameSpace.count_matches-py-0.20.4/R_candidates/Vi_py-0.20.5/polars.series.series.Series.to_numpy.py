    def to_numpy(
        self,
        *args: Any,
        zero_copy_only: bool = False,
        writable: bool = False,
        use_pyarrow: bool = True,
    ) -> np.ndarray[Any, Any]:
        """
        Convert this Series to numpy.

        This operation may clone data but is completely safe. Note that:

        - data which is purely numeric AND without null values is not cloned;
        - floating point `nan` values can be zero-copied;
        - booleans can't be zero-copied.

        To ensure that no data is cloned, set `zero_copy_only=True`.

        Parameters
        ----------
        *args
            args will be sent to pyarrow.Array.to_numpy.
        zero_copy_only
            If True, an exception will be raised if the conversion to a numpy
            array would require copying the underlying data (e.g. in presence
            of nulls, or for non-primitive types).
        writable
            For numpy arrays created with zero copy (view on the Arrow data),
            the resulting array is not writable (Arrow data is immutable).
            By setting this to True, a copy of the array is made to ensure
            it is writable.
        use_pyarrow
            Use `pyarrow.Array.to_numpy
            <https://arrow.apache.org/docs/python/generated/pyarrow.Array.html#pyarrow.Array.to_numpy>`_

            for the conversion to numpy.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> arr = s.to_numpy()
        >>> arr  # doctest: +IGNORE_RESULT
        array([1, 2, 3], dtype=int64)
        >>> type(arr)
        <class 'numpy.ndarray'>
        """

        def convert_to_date(arr: np.ndarray[Any, Any]) -> np.ndarray[Any, Any]:
            if self.dtype == Date:
                tp = "datetime64[D]"
            elif self.dtype == Duration:
                tp = f"timedelta64[{self.dtype.time_unit}]"  # type: ignore[attr-defined]
            else:
                tp = f"datetime64[{self.dtype.time_unit}]"  # type: ignore[attr-defined]
            return arr.astype(tp)

        def raise_no_zero_copy() -> None:
            if zero_copy_only:
                msg = "cannot return a zero-copy array"
                raise ValueError(msg)

        if self.dtype == Array:
            np_array = self.explode().to_numpy(
                zero_copy_only=zero_copy_only,
                writable=writable,
                use_pyarrow=use_pyarrow,
            )
            np_array.shape = (self.len(), self.dtype.width)  # type: ignore[attr-defined]
            return np_array

        if (
            use_pyarrow
            and _PYARROW_AVAILABLE
            and self.dtype != Object
            and (self.dtype == Time or not self.dtype.is_temporal())
        ):
            return self.to_arrow().to_numpy(
                *args, zero_copy_only=zero_copy_only, writable=writable
            )

        elif self.dtype in (Time, Decimal):
            raise_no_zero_copy()
            # note: there are no native numpy "time" or "decimal" dtypes
            return np.array(self.to_list(), dtype="object")
        else:
            if not self.null_count():
                if self.dtype.is_temporal():
                    np_array = convert_to_date(self._view(ignore_nulls=True))
                elif self.dtype.is_numeric():
                    np_array = self._view(ignore_nulls=True)
                else:
                    raise_no_zero_copy()
                    np_array = self._s.to_numpy()

            elif self.dtype.is_temporal():
                np_array = convert_to_date(self.to_physical()._s.to_numpy())
            else:
                raise_no_zero_copy()
                np_array = self._s.to_numpy()

            if writable and not np_array.flags.writeable:
                raise_no_zero_copy()
                return np_array.copy()
            else:
                return np_array
