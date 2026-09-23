    def __eq__(self, other):
        if isinstance(other, pyarrow.BaseExtensionType):
            return (
                type(self) == type(other)
                and self.subtype == other.subtype
                and self.closed == other.closed
            )
        else:
            return NotImplemented
