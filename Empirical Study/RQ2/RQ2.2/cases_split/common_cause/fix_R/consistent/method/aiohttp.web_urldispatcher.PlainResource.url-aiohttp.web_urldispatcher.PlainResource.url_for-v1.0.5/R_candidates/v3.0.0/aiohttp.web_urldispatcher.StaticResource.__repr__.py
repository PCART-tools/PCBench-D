    def __repr__(self):
        name = "'" + self.name + "'" if self.name is not None else ""
        return "<StaticResource {name} {path} -> {directory!r}".format(
            name=name, path=self._prefix, directory=self._directory)
