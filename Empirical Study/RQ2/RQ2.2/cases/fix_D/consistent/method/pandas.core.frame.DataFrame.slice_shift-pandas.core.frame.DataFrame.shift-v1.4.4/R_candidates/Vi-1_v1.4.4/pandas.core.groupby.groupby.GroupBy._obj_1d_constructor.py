    @final
    @property
    def _obj_1d_constructor(self) -> Callable:
        # GH28330 preserve subclassed Series/DataFrames
        if isinstance(self.obj, DataFrame):
            return self.obj._constructor_sliced
        assert isinstance(self.obj, Series)
        return self.obj._constructor
