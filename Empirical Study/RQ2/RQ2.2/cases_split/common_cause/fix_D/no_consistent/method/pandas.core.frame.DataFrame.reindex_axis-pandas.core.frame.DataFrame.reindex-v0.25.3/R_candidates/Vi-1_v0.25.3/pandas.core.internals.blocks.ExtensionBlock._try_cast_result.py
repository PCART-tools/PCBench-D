    def _try_cast_result(self, result, dtype=None):
        """
        if we have an operation that operates on for example floats
        we want to try to cast back to our EA here if possible

        result could be a 2-D numpy array, e.g. the result of
        a numeric operation; but it must be shape (1, X) because
        we by-definition operate on the ExtensionBlocks one-by-one

        result could also be an EA Array itself, in which case it
        is already a 1-D array
        """
        try:

            result = self._holder._from_sequence(result.ravel(), dtype=dtype)
        except Exception:
            pass

        return result
