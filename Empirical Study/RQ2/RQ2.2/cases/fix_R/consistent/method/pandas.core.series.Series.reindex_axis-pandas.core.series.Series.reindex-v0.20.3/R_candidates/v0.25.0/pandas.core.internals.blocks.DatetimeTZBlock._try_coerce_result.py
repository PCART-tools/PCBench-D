    def _try_coerce_result(self, result):
        """ reverse of try_coerce_args """
        if isinstance(result, np.ndarray):
            if result.dtype.kind in ["i", "f"]:
                result = result.astype("M8[ns]")

        elif isinstance(result, (np.integer, np.float, np.datetime64)):
            result = self._box_func(result)

        if isinstance(result, np.ndarray):
            # allow passing of > 1dim if its trivial

            if result.ndim > 1:
                result = result.reshape(np.prod(result.shape))
            # GH#24096 new values invalidates a frequency
            result = self._holder._simple_new(
                result, freq=None, dtype=self.values.dtype
            )

        return result
