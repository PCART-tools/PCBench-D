    @property
    def shape(self):
        """ Shape of the Categorical.

        For internal compatibility with numpy arrays.

        Returns
        -------
        shape : tuple
        """

        return tuple([len(self._codes)])
