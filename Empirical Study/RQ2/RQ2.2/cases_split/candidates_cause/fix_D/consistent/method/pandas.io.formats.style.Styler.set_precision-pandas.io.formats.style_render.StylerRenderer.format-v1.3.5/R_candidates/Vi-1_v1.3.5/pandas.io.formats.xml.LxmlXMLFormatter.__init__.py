    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.validate_columns()
        self.validate_encoding()
        self.prefix_uri = self.get_prefix_uri()

        self.convert_empty_str_key()
        self.handle_indexes()
