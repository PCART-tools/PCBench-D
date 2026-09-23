    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__module__}.{self.__class__.__name__} "
            f"image mode={self.mode} size={self.size[0]}x{self.size[1]} "
            f"at 0x{id(self):X}>"
        )
