    def __eq__(self, other):
        return (
            self.__class__ is other.__class__
            and self.mode == other.mode
            and self.size == other.size
            and self.info == other.info
            and self.getpalette() == other.getpalette()
            and self.tobytes() == other.tobytes()
        )
