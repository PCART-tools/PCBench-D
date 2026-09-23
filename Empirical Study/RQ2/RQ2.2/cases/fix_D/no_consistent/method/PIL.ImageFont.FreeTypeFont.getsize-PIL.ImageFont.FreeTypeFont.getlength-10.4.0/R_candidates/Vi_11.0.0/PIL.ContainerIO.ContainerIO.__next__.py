    def __next__(self) -> AnyStr:
        line = self.readline()
        if not line:
            msg = "end of region"
            raise StopIteration(msg)
        return line
