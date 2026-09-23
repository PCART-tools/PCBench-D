    @classmethod
    def _concat_same_type(cls, to_concat) -> ArrowStringArray:
        """
        Concatenate multiple ArrowStringArray.

        Parameters
        ----------
        to_concat : sequence of ArrowStringArray

        Returns
        -------
        ArrowStringArray
        """
        return cls(
            pa.chunked_array(
                [array for ea in to_concat for array in ea._data.iterchunks()]
            )
        )
