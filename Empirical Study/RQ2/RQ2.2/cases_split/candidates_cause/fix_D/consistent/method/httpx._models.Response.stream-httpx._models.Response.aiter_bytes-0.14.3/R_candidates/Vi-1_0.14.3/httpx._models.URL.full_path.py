    @property
    def full_path(self) -> str:
        path = self.path
        if self.query:
            path += "?" + self.query
        return path
