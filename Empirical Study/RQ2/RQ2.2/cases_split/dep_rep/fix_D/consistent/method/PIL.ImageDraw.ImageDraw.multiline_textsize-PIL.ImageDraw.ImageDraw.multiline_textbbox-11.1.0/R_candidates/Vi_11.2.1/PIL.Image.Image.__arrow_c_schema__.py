    def __arrow_c_schema__(self) -> object:
        self.load()
        return self.im.__arrow_c_schema__()
