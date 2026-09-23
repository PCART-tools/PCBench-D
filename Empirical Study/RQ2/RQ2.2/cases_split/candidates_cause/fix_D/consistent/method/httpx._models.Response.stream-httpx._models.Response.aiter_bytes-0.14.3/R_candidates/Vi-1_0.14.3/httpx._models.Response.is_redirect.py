    @property
    def is_redirect(self) -> bool:
        return codes.is_redirect(self.status_code) and "location" in self.headers
