        def __init__(
            self,
            function: Callable[[Series], Series | Any],
            return_dtype: PolarsDataType | None,
        ):
            self.function = function
            self.return_dtype = return_dtype
