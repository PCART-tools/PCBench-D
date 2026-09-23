    @cached_property
    def layers(self):
        layers = []
        if self._layers_position is not None:
            self._fp.seek(self._layers_position)
            _layer_data = io.BytesIO(ImageFile._safe_read(self._fp, self._layers_size))
            layers = _layerinfo(_layer_data, self._layers_size)
        self._n_frames = len(layers)
        return layers
