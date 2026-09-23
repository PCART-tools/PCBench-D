    def __init__(
        self,
        values: np.ndarray | TimedeltaIndex,
        nat_rep: str = "NaT",
        box: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(values, **kwargs)
        self.nat_rep = nat_rep
        self.box = box
