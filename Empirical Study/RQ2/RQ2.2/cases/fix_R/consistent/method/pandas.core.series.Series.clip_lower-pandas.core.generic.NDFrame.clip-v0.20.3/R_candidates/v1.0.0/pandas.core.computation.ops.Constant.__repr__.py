    def __repr__(self) -> str:
        # in python 2 str() of float
        # can truncate shorter than repr()
        return repr(self.name)
