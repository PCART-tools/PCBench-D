    def _write_clips(self):
        if not len(self._clipd):
            return
        writer = self.writer
        writer.start('defs')
        for clip, oid in self._clipd.values():
            writer.start('clipPath', id=oid)
            if len(clip) == 2:
                clippath, clippath_trans = clip
                path_data = self._convert_path(
                    clippath, clippath_trans, simplify=False)
                writer.element('path', d=path_data)
            else:
                x, y, w, h = clip
                writer.element(
                    'rect',
                    x=short_float_fmt(x),
                    y=short_float_fmt(y),
                    width=short_float_fmt(w),
                    height=short_float_fmt(h))
            writer.end('clipPath')
        writer.end('defs')
