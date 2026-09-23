    def __repr__(self) -> str_type:
        if self.categories is None:
            data = "None"
            dtype = "None"
        else:
            data = self.categories._format_data(name=type(self).__name__)
            if data is None:
                # self.categories is RangeIndex
                data = str(self.categories._range)
            data = data.rstrip(", ")
            dtype = self.categories.dtype

        return (
            f"CategoricalDtype(categories={data}, ordered={self.ordered}, "
            f"categories_dtype={dtype})"
        )
