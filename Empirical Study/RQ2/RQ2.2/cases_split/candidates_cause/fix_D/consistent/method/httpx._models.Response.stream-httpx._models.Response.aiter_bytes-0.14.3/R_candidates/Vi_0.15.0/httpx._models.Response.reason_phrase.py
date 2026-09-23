    @property
    def reason_phrase(self) -> str:
        return self.ext.get("reason", codes.get_reason_phrase(self.status_code))
