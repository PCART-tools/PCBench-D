        def __eq__(self, other):
            if isinstance(other, pyarrow.BaseExtensionType):
                return type(self) == type(other) and self.freq == other.freq
            else:
                return NotImplemented
