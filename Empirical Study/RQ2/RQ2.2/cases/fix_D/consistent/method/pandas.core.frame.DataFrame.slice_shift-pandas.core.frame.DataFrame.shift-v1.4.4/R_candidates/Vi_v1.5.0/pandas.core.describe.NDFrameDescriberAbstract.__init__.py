    def __init__(self, obj: DataFrame | Series, datetime_is_numeric: bool) -> None:
        self.obj = obj
        self.datetime_is_numeric = datetime_is_numeric
