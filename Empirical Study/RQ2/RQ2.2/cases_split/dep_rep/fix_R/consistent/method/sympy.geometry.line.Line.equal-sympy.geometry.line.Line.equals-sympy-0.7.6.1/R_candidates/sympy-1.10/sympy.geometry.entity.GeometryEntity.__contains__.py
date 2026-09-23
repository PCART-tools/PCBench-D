    def __contains__(self, other):
        """Subclasses should implement this method for anything more complex than equality."""
        if type(self) is type(other):
            return self == other
        raise NotImplementedError()
