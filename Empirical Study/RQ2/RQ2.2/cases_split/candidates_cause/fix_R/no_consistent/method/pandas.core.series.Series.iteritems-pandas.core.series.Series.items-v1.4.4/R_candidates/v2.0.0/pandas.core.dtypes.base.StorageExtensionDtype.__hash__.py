    def __hash__(self) -> int:
        # custom __eq__ so have to override __hash__
        return super().__hash__()
