    def seek(self, layer: int) -> None:
        if not self._seek_check(layer):
            return
        if isinstance(self._fp, DeferredError):
            raise self._fp.ex

        # seek to given layer (1..max)
        _, mode, _, tile = self.layers[layer - 1]
        self._mode = mode
        self.tile = tile
        self.frame = layer
        self.fp = self._fp
