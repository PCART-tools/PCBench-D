    def get(self, label, default=None):
        """
        Returns value occupying requested label, default to specified
        missing value if not present. Analogous to dict.get

        Parameters
        ----------
        label : object
            Label value looking for
        default : object, optional
            Value to return if label not in index

        Returns
        -------
        y : scalar
        """
        try:
            return self.get_value(label)
        except KeyError:
            return default
