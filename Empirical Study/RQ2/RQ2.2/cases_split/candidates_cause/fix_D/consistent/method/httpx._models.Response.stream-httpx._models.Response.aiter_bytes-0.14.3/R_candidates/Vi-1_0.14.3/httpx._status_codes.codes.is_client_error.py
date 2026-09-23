    @classmethod
    def is_client_error(cls, value: int) -> bool:
        return 400 <= value <= 499
