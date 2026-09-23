    @property
    def is_relative_url(self) -> bool:
        return not self.is_absolute_url
