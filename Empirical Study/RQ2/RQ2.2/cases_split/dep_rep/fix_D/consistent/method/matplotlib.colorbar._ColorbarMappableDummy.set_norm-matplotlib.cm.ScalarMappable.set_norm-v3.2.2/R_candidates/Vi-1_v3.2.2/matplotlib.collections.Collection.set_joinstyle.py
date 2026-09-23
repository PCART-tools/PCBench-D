    def set_joinstyle(self, js):
        """
        Set the joinstyle for the collection (for all its elements).

        Parameters
        ----------
        js : {'miter', 'round', 'bevel'}
            The joinstyle
        """
        cbook._check_in_list(('miter', 'round', 'bevel'), joinstyle=js)
        self._joinstyle = js
