    def _to_embed(self, keep_tz=False, dtype=None):
        """
        return an array repr of this object, potentially casting to object

        This is for internal compat
        """
        if dtype is not None:
            return self.astype(dtype)._to_embed(keep_tz=keep_tz)

        if keep_tz and self.tz is not None:

            # preserve the tz & copy
            return self.copy(deep=True)

        return self.values.copy()
