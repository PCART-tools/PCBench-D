    def __init__(
        self,
        values: np.ndarray | Series | DatetimeIndex | DatetimeArray,
        nat_rep: str = "NaT",
        date_format: None = None,
        **kwargs,
    ) -> None:
        super().__init__(values, **kwargs)
        self.nat_rep = nat_rep
        self.date_format = date_format
