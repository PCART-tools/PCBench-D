    @property
    def is_error(self) -> bool:
        return codes.is_error(self.status_code)
