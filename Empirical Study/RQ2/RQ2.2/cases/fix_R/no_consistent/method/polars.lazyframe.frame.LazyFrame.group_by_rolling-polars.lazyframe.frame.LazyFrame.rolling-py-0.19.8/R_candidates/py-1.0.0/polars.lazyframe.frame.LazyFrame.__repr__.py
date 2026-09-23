    def __repr__(self) -> str:
        # don't expose internal/private classpath
        return f"<{self.__class__.__name__} at 0x{id(self):X}>"
