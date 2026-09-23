    def bestsize(self) -> tuple[int, int, int]:
        sizes = self.itersizes()
        if not sizes:
            msg = "No 32bit icon resources found"
            raise SyntaxError(msg)
        return max(sizes)
