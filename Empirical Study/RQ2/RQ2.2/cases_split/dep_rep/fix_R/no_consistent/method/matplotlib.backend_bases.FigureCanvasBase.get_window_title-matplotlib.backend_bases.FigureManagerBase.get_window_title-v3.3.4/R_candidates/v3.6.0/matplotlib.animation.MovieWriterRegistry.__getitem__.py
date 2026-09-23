    def __getitem__(self, name):
        """Get an available writer class from its name."""
        if self.is_available(name):
            return self._registered[name]
        raise RuntimeError(f"Requested MovieWriter ({name}) not available")
