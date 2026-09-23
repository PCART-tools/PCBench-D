    def set_joinstyle(self, js):
        """
        Set the joinstyle for the collection. The joinstyle can only be
        set globally for all elements in the collection.

        Parameters
        ----------
        js : {'miter', 'round', 'bevel'}
            The joinstyle
        """
        if js in ('miter', 'round', 'bevel'):
            self._joinstyle = js
        else:
            raise ValueError('Unrecognized join style.  Found %s' % js)
