    @property
    def named_transformers_(self):
        """Access the fitted transformer by name.

        Read-only attribute to access any transformer by given name.
        Keys are transformer names and values are the fitted transformer
        objects.
        """
        # Use Bunch object to improve autocomplete
        return Bunch(**{name: trans for name, trans, _ in self.transformers_})
