    def __repr__(self):
        return "<%s.%s image mode=%s size=%dx%d at 0x%X>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.mode,
            self.size[0],
            self.size[1],
            id(self),
        )
