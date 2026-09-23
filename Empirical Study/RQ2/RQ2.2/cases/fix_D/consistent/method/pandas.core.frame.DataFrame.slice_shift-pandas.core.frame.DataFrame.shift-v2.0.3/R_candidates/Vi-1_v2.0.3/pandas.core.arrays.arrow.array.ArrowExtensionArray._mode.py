    def _mode(self: ArrowExtensionArrayT, dropna: bool = True) -> ArrowExtensionArrayT:
        """
        Returns the mode(s) of the ExtensionArray.

        Always returns `ExtensionArray` even if only one value.

        Parameters
        ----------
        dropna : bool, default True
            Don't consider counts of NA values.

        Returns
        -------
        same type as self
            Sorted, if possible.
        """
        pa_type = self._data.type
        if pa.types.is_temporal(pa_type):
            nbits = pa_type.bit_width
            if nbits == 32:
                data = self._data.cast(pa.int32())
            elif nbits == 64:
                data = self._data.cast(pa.int64())
            else:
                raise NotImplementedError(pa_type)
        else:
            data = self._data

        if dropna:
            data = data.drop_null()

        res = pc.value_counts(data)
        most_common = res.field("values").filter(
            pc.equal(res.field("counts"), pc.max(res.field("counts")))
        )

        if pa.types.is_temporal(pa_type):
            most_common = most_common.cast(pa_type)

        return type(self)(most_common)
