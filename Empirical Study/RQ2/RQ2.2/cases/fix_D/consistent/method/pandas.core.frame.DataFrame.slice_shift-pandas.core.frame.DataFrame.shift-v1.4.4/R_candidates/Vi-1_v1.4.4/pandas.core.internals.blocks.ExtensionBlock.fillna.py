    def fillna(
        self, value, limit=None, inplace: bool = False, downcast=None
    ) -> list[Block]:
        values = self.values.fillna(value=value, limit=limit)
        return [self.make_block_same_class(values=values)]
