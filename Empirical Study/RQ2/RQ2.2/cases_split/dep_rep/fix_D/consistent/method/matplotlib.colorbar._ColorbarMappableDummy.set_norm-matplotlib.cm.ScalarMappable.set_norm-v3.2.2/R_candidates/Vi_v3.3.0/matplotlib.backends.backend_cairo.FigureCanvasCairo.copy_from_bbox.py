    def copy_from_bbox(self, bbox):
        surface = self._renderer.gc.ctx.get_target()
        if not isinstance(surface, cairo.ImageSurface):
            raise RuntimeError(
                "copy_from_bbox only works when rendering to an ImageSurface")
        sw = surface.get_width()
        sh = surface.get_height()
        x0 = math.ceil(bbox.x0)
        x1 = math.floor(bbox.x1)
        y0 = math.ceil(sh - bbox.y1)
        y1 = math.floor(sh - bbox.y0)
        if not (0 <= x0 and x1 <= sw and bbox.x0 <= bbox.x1
                and 0 <= y0 and y1 <= sh and bbox.y0 <= bbox.y1):
            raise ValueError("Invalid bbox")
        sls = slice(y0, y0 + max(y1 - y0, 0)), slice(x0, x0 + max(x1 - x0, 0))
        data = (np.frombuffer(surface.get_data(), np.uint32)
                .reshape((sh, sw))[sls].copy())
        return _CairoRegion(sls, data)
