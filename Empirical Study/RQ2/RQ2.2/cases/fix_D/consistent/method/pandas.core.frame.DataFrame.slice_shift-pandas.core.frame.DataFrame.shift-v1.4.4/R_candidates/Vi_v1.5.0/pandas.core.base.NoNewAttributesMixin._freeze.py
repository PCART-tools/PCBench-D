    def _freeze(self):
        """
        Prevents setting additional attributes.
        """
        object.__setattr__(self, "__frozen", True)
