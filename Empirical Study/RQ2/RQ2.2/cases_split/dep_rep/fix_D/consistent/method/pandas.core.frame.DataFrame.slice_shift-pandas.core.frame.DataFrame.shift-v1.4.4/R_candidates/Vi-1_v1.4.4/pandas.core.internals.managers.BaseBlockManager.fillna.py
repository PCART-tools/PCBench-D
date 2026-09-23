    def fillna(self: T, value, limit, inplace: bool, downcast) -> T:
        return self.apply(
            "fillna", value=value, limit=limit, inplace=inplace, downcast=downcast
        )
