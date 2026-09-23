    def set_output(self, transform=None):
        # This transformer will always output a DataFrame regardless of the
        # configuration.
        return self
