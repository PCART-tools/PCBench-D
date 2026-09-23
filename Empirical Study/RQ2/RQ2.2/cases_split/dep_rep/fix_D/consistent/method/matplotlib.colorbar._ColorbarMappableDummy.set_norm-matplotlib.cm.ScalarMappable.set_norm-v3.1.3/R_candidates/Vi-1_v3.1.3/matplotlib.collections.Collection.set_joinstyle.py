    def set_joinstyle(self, js):
        """
        Set the joinstyle for the collection (for all its elements).

        Parameters
        ----------
        js : {'miter', 'round', 'bevel'}
            The joinstyle
        """
        if js in ('miter', 'round', 'bevel'):
            self._joinstyle = js
        else:
            raise ValueError('Unrecognized join style.  Found %s' % js)
