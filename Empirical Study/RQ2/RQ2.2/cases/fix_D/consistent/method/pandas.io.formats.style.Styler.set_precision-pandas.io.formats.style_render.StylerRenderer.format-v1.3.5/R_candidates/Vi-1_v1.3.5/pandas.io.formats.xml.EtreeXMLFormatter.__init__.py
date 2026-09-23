    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.validate_columns()
        self.validate_encoding()
        self.handle_indexes()
        self.prefix_uri = self.get_prefix_uri()
