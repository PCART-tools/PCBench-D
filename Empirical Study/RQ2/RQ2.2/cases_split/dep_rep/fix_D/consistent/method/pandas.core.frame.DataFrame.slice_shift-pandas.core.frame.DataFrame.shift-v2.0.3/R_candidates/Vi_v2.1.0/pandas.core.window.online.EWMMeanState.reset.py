    def reset(self) -> None:
        self.old_wt = np.ones(self.shape[self.axis - 1])
        self.last_ewm = None
