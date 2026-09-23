    def set_joinstyle(self, js):
        """Set the join style to be one of ('miter', 'round', 'bevel')."""
        if js in ('miter', 'round', 'bevel'):
            self._joinstyle = js
        else:
            raise ValueError('Unrecognized join style.  Found %s' % js)
