    def convert(
        self: T,
        copy: bool = True,
        datetime: bool = True,
        numeric: bool = True,
        timedelta: bool = True,
    ) -> T:
        return self.apply(
            "convert",
            copy=copy,
            datetime=datetime,
            numeric=numeric,
            timedelta=timedelta,
        )
