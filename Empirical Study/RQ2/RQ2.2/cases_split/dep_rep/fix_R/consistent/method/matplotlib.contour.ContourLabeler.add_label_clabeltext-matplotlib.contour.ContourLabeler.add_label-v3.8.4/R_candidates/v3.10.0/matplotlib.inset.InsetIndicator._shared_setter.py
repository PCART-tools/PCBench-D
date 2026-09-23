    def _shared_setter(self, prop, val):
        """
        Helper function to set the same style property on the artist and its children.
        """
        setattr(self, f'_{prop}', val)

        artist.setp([self._rectangle, *self._connectors], prop, val)
