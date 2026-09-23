    def unique(self) -> Self:
        """
        Compute the ArrowExtensionArray of unique values.

        Returns
        -------
        ArrowExtensionArray
        """
        pa_type = self._pa_array.type

        if pa_version_under11p0 and pa.types.is_duration(pa_type):
            # https://github.com/apache/arrow/issues/15226#issuecomment-1376578323
            data = self._pa_array.cast(pa.int64())
        else:
            data = self._pa_array

        pa_result = pc.unique(data)

        if pa_version_under11p0 and pa.types.is_duration(pa_type):
            pa_result = pa_result.cast(pa_type)

        return type(self)(pa_result)
