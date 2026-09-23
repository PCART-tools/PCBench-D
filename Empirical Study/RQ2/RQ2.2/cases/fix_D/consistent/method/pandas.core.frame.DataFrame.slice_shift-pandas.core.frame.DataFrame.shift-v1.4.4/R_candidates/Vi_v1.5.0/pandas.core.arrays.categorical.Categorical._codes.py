    @_codes.setter
    def _codes(self, value: np.ndarray):
        warn(
            "Setting the codes on a Categorical is deprecated and will raise in "
            "a future version. Create a new Categorical object instead",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )  # GH#40606
        NDArrayBacked.__init__(self, value, self.dtype)
