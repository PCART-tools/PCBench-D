    def seek(self, layer):
        if not self._seek_check(layer):
            return

        # seek to given layer (1..max)
        try:
            name, mode, bbox, tile = self.layers[layer - 1]
            self._mode = mode
            self.tile = tile
            self.frame = layer
            self.fp = self._fp
            return name, bbox
        except IndexError as e:
            msg = "no such layer"
            raise EOFError(msg) from e
