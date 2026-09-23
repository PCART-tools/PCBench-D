    def _replace_single(self, *args, **kwargs):
        """ no-op on a non-ObjectBlock """
        return self if kwargs["inplace"] else self.copy()
