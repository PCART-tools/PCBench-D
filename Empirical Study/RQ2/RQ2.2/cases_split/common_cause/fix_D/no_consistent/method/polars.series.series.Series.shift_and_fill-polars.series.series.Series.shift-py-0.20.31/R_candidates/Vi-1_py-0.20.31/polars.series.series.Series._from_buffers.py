    @classmethod
    def _from_buffers(
        cls,
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
              of type `Int64`. Note that this does not match how the data
              is represented internally and data copy is required to construct
              the Series.
        validity
            Validity buffer. If specified, must be a Series of data type `Boolean`.

        Returns
        -------
        Series

        Raises
        ------
        TypeError
            When the given `dtype` is not supported or the other inputs do not match
            the requirements for constructing a Series of the given `dtype`.

        Warnings
        --------
        Constructing a `String` Series requires specifying a values and offsets buffer,
        which does not match the actual underlying buffers. The values and offsets
        buffer are converted into the actual buffers, which copies data.

        Notes
        -----
        This method is mainly intended for use with the dataframe interchange protocol.
        """
        if isinstance(data, Series):
            data = [data._s]
        else:
            data = [s._s for s in data]
        if validity is not None:
            validity = validity._s
        return cls._from_pyseries(PySeries._from_buffers(dtype, data, validity))
