    def get_value(self, label):
        """
        Quickly retrieve single value at passed index label

        Parameters
        ----------
        index : label

        Returns
        -------
        value : scalar value
        """
        return self.index.get_value(self.values, label)
