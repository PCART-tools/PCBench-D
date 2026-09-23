    def _to_embed(self, keep_tz=False, dtype=None):
        """
        *this is an internal non-public method*

        return an array repr of this object, potentially casting to object

        """
        if dtype is not None:
            return self.astype(dtype)._to_embed(keep_tz=keep_tz)

        return self.values.copy()
