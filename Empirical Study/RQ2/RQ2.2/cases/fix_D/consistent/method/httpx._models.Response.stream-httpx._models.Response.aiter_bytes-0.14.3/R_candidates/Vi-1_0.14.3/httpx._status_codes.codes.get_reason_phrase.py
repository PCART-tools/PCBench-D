    @classmethod
    def get_reason_phrase(cls, value: int) -> str:
        try:
            return codes(value).phrase  # type: ignore
        except ValueError:
            return ""
