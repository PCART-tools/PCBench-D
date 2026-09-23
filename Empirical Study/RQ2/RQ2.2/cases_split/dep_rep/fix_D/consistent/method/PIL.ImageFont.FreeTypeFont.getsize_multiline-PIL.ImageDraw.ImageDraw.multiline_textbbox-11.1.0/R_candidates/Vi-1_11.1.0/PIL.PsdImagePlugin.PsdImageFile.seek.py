    def seek(self, layer: int) -> None:
        if not self._seek_check(layer):
            return

        # seek to given layer (1..max)
        try:
            _, mode, _, tile = self.layers[layer - 1]
            self._mode = mode
            self.tile = tile
            self.frame = layer
            self.fp = self._fp
        except IndexError as e:
            msg = "no such layer"
            raise EOFError(msg) from e
