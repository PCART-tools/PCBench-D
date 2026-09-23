    @classmethod
    def _from_buffers(
        self,
        dtype: PolarsDataType,
        data: Series | Sequence[Series],
        validity: Series | None = None,
    ) -> Self:
        """
        Construct a Series from information about its underlying buffers.

        Parameters
        ----------
        dtype
            The data type of the resulting Series.
        data
            Buffers describing the data. For most data types, this is a single Series of
            the physical data type of `dtype`. Some data types require multiple buffers:

            - `String`: A data buffer of type `UInt8` and an offsets buffer
                        of type `Int64`.
        validity
            Validity buffer. If specified, must be a Series of data type `Boolean`.

        Returns
        -------
        Series
        """
        if isinstance(data, Series):
            data = [data._s]
        else:
            data = [s._s for s in data]
        if validity is not None:
            validity = validity._s
        return self._from_pyseries(PySeries._from_buffers(dtype, data, validity))
