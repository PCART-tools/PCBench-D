    def _validate_dtype(self, dtype):
        """ validate the passed dtype """

        if dtype is not None:
            dtype = pandas_dtype(dtype)

            # a compound dtype
            if dtype.kind == "V":
                raise NotImplementedError(
                    "compound dtypes are not implemented"
                    f" in the {type(self).__name__} constructor"
                )

        return dtype
