    def _construct_result(
        self, result: ArrayLike | tuple[ArrayLike, ArrayLike], name: Hashable
    ) -> Series | tuple[Series, Series]:
        """
        Construct an appropriately-labelled Series from the result of an op.

        Parameters
        ----------
        result : ndarray or ExtensionArray
        name : Label

        Returns
        -------
        Series
            In the case of __divmod__ or __rdivmod__, a 2-tuple of Series.
        """
        if isinstance(result, tuple):
            # produced by divmod or rdivmod

            res1 = self._construct_result(result[0], name=name)
            res2 = self._construct_result(result[1], name=name)

            # GH#33427 assertions to keep mypy happy
            assert isinstance(res1, Series)
            assert isinstance(res2, Series)
            return (res1, res2)

        # TODO: result should always be ArrayLike, but this fails for some
        #  JSONArray tests
        dtype = getattr(result, "dtype", None)
        out = self._constructor(result, index=self.index, dtype=dtype)
        out = out.__finalize__(self)

        # Set the result's name after __finalize__ is called because __finalize__
        #  would set it back to self.name
        out.name = name
        return out
