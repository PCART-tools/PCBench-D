    def insert(self, loc: int, item) -> ArrowStringArray:
        if not isinstance(item, str) and item is not libmissing.NA:
            raise TypeError("Scalar must be NA or str")
        return super().insert(loc, item)
