    @property
    def n_frames(self) -> int:
        if self._n_frames is None:
            self._n_frames = len(self.layers)
        return self._n_frames
