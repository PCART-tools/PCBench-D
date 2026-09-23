    def __hash__(self) -> int:
        # make myself hashable
        return hash(str(self))
