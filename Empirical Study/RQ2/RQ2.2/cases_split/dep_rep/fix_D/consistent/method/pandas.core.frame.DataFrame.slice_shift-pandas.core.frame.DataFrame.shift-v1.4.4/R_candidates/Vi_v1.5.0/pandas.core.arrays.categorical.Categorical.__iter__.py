    def __iter__(self):
        """
        Returns an Iterator over the values of this Categorical.
        """
        if self.ndim == 1:
            return iter(self._internal_get_values().tolist())
        else:
            return (self[n] for n in range(len(self)))
