    @property
    def series_generator(self):
        constructor = self.obj._constructor_sliced
        return (
            constructor(arr, index=self.columns, name=name)
            for i, (arr, name) in enumerate(zip(self.values, self.index))
        )
