    def set_segments(self, segments):
        if segments is None:
            return
        _segments = []

        for seg in segments:
            if not isinstance(seg, np.ma.MaskedArray):
                seg = np.asarray(seg, float)
            _segments.append(seg)

        self._paths = [mpath.Path(_seg) for _seg in _segments]
        self.stale = True
