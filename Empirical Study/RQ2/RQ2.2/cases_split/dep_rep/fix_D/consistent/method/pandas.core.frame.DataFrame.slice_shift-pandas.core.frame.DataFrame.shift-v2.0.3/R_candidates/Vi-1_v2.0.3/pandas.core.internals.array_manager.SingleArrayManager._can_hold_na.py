    @property
    def _can_hold_na(self) -> bool:
        if isinstance(self.array, np.ndarray):
            return self.array.dtype.kind not in ["b", "i", "u"]
        else:
            # ExtensionArray
            return self.array._can_hold_na
