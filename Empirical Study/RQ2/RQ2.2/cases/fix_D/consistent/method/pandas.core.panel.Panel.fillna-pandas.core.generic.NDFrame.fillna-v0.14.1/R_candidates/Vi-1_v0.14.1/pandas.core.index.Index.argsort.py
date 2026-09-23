    def argsort(self, *args, **kwargs):
        """
        See docstring for ndarray.argsort
        """
        result = self.asi8
        if result is None:
            result = self.view(np.ndarray)
        return result.argsort(*args, **kwargs)
