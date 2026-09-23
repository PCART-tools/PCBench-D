    def _write_hatches(self):
        if not len(self._hatchd):
            return
        HATCH_SIZE = 72
        writer = self.writer
        writer.start('defs')
        for (path, face, stroke), oid in self._hatchd.values():
            writer.start(
                'pattern',
                id=oid,
                patternUnits="userSpaceOnUse",
                x="0", y="0", width=str(HATCH_SIZE),
                height=str(HATCH_SIZE))
            path_data = self._convert_path(
                path,
                Affine2D()
                .scale(HATCH_SIZE).scale(1.0, -1.0).translate(0, HATCH_SIZE),
                simplify=False)
            if face is None:
                fill = 'none'
            else:
                fill = rgb2hex(face)
            writer.element(
                'rect',
                x="0", y="0", width=str(HATCH_SIZE+1),
                height=str(HATCH_SIZE+1),
                fill=fill)
            writer.element(
                'path',
                d=path_data,
                style=generate_css({
                    'fill': rgb2hex(stroke),
                    'stroke': rgb2hex(stroke),
                    'stroke-width': str(rcParams['hatch.linewidth']),
                    'stroke-linecap': 'butt',
                    'stroke-linejoin': 'miter'
                    })
                )
            writer.end('pattern')
        writer.end('defs')
