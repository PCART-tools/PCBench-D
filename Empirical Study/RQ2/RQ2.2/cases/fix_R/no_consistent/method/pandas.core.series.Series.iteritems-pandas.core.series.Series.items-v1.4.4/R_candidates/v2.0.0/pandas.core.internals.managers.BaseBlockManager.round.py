    def round(self: T, decimals: int, using_cow: bool = False) -> T:
        return self.apply(
            "round",
            decimals=decimals,
            using_cow=using_cow,
        )
