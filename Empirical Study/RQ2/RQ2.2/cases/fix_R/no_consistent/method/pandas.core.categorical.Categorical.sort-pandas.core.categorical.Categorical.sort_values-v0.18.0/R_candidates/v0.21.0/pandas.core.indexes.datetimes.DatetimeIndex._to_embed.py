    def _to_embed(self, keep_tz=False):
        """
        return an array repr of this object, potentially casting to object

        This is for internal compat
        """
        if keep_tz and self.tz is not None:

            # preserve the tz & copy
            return self.copy(deep=True)

        return self.values.copy()
