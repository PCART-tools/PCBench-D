    @classmethod
    def _concat_same_type(
        cls: type[ArrowExtensionArrayT], to_concat
    ) -> ArrowExtensionArrayT:
        """
        Concatenate multiple ArrowExtensionArrays.

        Parameters
        ----------
        to_concat : sequence of ArrowExtensionArrays

        Returns
        -------
        ArrowExtensionArray
        """
        chunks = [array for ea in to_concat for array in ea._data.iterchunks()]
        arr = pa.chunked_array(chunks)
        return cls(arr)
