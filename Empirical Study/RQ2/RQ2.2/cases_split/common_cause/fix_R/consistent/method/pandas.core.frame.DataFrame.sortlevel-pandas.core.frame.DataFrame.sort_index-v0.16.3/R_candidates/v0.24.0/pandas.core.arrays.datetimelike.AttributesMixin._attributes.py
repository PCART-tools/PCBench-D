    @property
    def _attributes(self):
        # Inheriting subclass should implement _attributes as a list of strings
        raise AbstractMethodError(self)
