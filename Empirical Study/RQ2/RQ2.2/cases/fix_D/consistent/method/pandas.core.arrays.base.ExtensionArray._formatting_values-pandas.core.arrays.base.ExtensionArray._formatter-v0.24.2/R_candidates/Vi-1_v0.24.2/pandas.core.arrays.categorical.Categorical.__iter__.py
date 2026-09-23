    def __iter__(self):
        """
        Returns an Iterator over the values of this Categorical.
        """
        return iter(self.get_values().tolist())
