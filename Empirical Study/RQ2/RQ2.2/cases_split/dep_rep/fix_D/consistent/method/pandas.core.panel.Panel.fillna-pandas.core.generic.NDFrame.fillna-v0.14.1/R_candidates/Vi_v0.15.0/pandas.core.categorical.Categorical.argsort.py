    def argsort(self, ascending=True, **kwargs):
        """ Implements ndarray.argsort.

        For internal compatibility with numpy arrays.

        Only ordered Categoricals can be argsorted!

        Returns
        -------
        argsorted : numpy array
        """
        if not self.ordered:
            raise TypeError("Categorical not ordered")
        result = np.argsort(self._codes.copy(), **kwargs)
        if not ascending:
            result = result[::-1]
        return result
