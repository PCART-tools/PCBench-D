    @property
    def win_type(self):
        if self._win_freq_i8 is not None:
            warnings.warn(
                "win_type will no longer return 'freq' in a future version. "
                "Check the type of self.window instead.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            return "freq"
        return self._win_type
