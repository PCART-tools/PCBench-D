    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.convert_empty_str_key()
