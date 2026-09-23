    def get_prop_tup(self, renderer=None):
        """
        Return a hashable tuple of properties.

        Not intended to be human readable, but useful for backends who
        want to cache derived information about text (e.g., layouts) and
        need to know if the text has changed.
        """
        props = [p for p in Text.get_prop_tup(self, renderer=renderer)]
        props.extend([self._x, self._y, self._dashlength,
                      self._dashdirection, self._dashrotation, self._dashpad,
                      self._dashpush])
        return tuple(props)
