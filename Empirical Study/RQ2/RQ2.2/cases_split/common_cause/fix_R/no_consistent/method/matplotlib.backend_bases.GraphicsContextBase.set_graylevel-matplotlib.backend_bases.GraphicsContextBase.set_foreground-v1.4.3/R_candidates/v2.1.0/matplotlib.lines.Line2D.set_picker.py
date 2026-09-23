    def set_picker(self, p):
        """Sets the event picker details for the line.

        ACCEPTS: float distance in points or callable pick function
        ``fn(artist, event)``
        """
        if callable(p):
            self._contains = p
        else:
            self.pickradius = p
        self._picker = p
