    def __eq__(self, other: object) -> bool:
        if self.__class__ is not other.__class__:
            return False
        assert isinstance(other, IndirectReference)
        return other.object_id == self.object_id and other.generation == self.generation
