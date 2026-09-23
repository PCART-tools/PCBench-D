    @property
    def raw(self) -> str:
        return f"{type(self).__name__}(name={repr(self.name)}, type={self.type})"
