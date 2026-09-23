    @classmethod
    def _box_pa_array(
        cls, value, pa_type: pa.DataType | None = None, copy: bool = False
    ) -> pa.Array | pa.ChunkedArray:
        """
        Box value into a pyarrow Array or ChunkedArray.

        Parameters
        ----------
        value : Sequence
        pa_type : pa.DataType | None

        Returns
        -------
        pa.Array or pa.ChunkedArray
        """
        if isinstance(value, cls):
            pa_array = value._pa_array
        elif isinstance(value, (pa.Array, pa.ChunkedArray)):
            pa_array = value
        elif isinstance(value, BaseMaskedArray):
            # GH 52625
            if copy:
                value = value.copy()
            pa_array = value.__arrow_array__()
        else:
            if (
                isinstance(value, np.ndarray)
                and pa_type is not None
                and (
                    pa.types.is_large_binary(pa_type)
                    or pa.types.is_large_string(pa_type)
                )
            ):
                # See https://github.com/apache/arrow/issues/35289
                value = value.tolist()
            elif copy and is_array_like(value):
                # pa array should not get updated when numpy array is updated
                value = value.copy()

            if (
                pa_type is not None
                and pa.types.is_duration(pa_type)
                and (not isinstance(value, np.ndarray) or value.dtype.kind not in "mi")
            ):
                # Workaround https://github.com/apache/arrow/issues/37291
                from pandas.core.tools.timedeltas import to_timedelta

                value = to_timedelta(value, unit=pa_type.unit).as_unit(pa_type.unit)
                value = value.to_numpy()

            try:
                pa_array = pa.array(value, type=pa_type, from_pandas=True)
            except pa.ArrowInvalid:
                # GH50430: let pyarrow infer type, then cast
                pa_array = pa.array(value, from_pandas=True)

            if pa_type is None and pa.types.is_duration(pa_array.type):
                # Workaround https://github.com/apache/arrow/issues/37291
                from pandas.core.tools.timedeltas import to_timedelta

                value = to_timedelta(value)
                value = value.to_numpy()
                pa_array = pa.array(value, type=pa_type, from_pandas=True)

            if pa.types.is_duration(pa_array.type) and pa_array.null_count > 0:
                # GH52843: upstream bug for duration types when originally
                # constructed with data containing numpy NaT.
                # https://github.com/apache/arrow/issues/35088
                arr = cls(pa_array)
                arr = arr.fillna(arr.dtype.na_value)
                pa_array = arr._pa_array

        if pa_type is not None and pa_array.type != pa_type:
            if pa.types.is_dictionary(pa_type):
                pa_array = pa_array.dictionary_encode()
            else:
                pa_array = pa_array.cast(pa_type)

        return pa_array
