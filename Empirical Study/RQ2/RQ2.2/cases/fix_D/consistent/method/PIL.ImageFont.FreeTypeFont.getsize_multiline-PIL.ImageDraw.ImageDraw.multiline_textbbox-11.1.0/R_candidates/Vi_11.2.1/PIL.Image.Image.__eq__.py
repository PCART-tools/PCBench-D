    def __eq__(self, other: object) -> bool:
        if self.__class__ is not other.__class__:
            return False
        assert isinstance(other, Image)
        return (
            self.mode == other.mode
            and self.size == other.size
            and self.info == other.info
            and self.getpalette() == other.getpalette()
            and self.tobytes() == other.tobytes()
        )
