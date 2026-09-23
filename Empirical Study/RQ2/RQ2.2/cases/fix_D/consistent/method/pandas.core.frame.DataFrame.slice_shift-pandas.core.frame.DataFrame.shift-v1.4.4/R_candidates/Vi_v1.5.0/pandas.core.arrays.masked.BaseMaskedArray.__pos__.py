    def __pos__(self: BaseMaskedArrayT) -> BaseMaskedArrayT:
        return self.copy()
