    def round(self: T, decimals: int, using_cow: bool = False) -> T:
        return self.apply_with_block("round", decimals=decimals, using_cow=using_cow)
