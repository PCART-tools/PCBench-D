    @property
    def asi8(self) -> np.ndarray:
        # do not cache or you'll create a memory leak
        return self.values.view("i8")
