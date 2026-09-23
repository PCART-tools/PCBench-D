    def __getattr__(self, elt: str) -> NoReturn:
        raise self.ex
