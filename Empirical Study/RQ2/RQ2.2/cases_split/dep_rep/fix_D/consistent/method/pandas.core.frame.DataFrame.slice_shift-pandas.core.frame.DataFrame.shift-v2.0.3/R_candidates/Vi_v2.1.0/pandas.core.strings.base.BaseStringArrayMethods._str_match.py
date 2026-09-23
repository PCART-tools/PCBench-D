    @abc.abstractmethod
    def _str_match(
        self, pat: str, case: bool = True, flags: int = 0, na: Scalar = np.nan
    ):
        pass
