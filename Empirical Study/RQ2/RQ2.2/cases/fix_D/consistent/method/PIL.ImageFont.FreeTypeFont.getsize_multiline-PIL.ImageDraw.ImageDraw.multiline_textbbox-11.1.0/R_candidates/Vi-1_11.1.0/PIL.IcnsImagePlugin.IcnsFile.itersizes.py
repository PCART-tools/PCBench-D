    def itersizes(self) -> list[tuple[int, int, int]]:
        sizes = []
        for size, fmts in self.SIZES.items():
            for fmt, reader in fmts:
                if fmt in self.dct:
                    sizes.append(size)
                    break
        return sizes
