    def copy(self):
        """Return a copy of self."""
        new = type(self)()
        vars(new).update(vars(self))
        return new
