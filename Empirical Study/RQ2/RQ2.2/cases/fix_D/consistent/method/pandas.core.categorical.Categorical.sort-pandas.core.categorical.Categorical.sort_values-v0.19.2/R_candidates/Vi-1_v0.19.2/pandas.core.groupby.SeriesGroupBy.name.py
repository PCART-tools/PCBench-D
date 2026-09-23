    @property
    def name(self):
        """
        since we are a series, we by definition only have
        a single name, but may be the result of a selection or
        the name of our object
        """
        if self._selection is None:
            return self.obj.name
        else:
            return self._selection
