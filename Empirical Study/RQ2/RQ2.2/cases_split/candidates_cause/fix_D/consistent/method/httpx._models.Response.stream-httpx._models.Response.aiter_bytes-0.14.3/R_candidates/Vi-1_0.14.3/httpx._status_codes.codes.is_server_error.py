    @classmethod
    def is_server_error(cls, value: int) -> bool:
        return 500 <= value <= 599
