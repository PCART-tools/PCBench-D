    def locally_modified_subplot_params(self):
        return [k for k in self._AllowedKeys if getattr(self, k)]
