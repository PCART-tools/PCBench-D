    def locally_modified_subplot_params(self):
        """
        Return a list of the names of the subplot parameters explicitly set
        in the GridSpec.

        This is a subset of the attributes of `.SubplotParams`.
        """
        return [k for k in self._AllowedKeys if getattr(self, k)]
