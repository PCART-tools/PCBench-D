    @final
    def round(self, decimals: int, using_cow: bool = False) -> Self:
        return self.apply_with_block(
            "round",
            decimals=decimals,
            using_cow=using_cow,
        )
