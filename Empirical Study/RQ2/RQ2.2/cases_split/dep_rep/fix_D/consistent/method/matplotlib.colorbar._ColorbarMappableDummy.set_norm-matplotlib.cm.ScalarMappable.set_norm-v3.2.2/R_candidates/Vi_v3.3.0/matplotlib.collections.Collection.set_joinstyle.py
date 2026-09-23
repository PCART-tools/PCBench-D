    def set_joinstyle(self, js):
        """
        Set the joinstyle for the collection (for all its elements).

        Parameters
        ----------
        js : {'miter', 'round', 'bevel'}
            The joinstyle.
        """
        mpl.rcsetup.validate_joinstyle(js)
        self._joinstyle = js
