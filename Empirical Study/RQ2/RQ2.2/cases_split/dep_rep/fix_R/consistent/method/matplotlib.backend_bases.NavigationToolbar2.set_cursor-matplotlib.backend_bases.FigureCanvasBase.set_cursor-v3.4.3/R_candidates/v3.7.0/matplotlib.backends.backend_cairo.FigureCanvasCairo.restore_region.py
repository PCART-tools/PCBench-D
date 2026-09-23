    def restore_region(self, region):
        surface = self._renderer.gc.ctx.get_target()
        if not isinstance(surface, cairo.ImageSurface):
            raise RuntimeError(
                "restore_region only works when rendering to an ImageSurface")
        surface.flush()
        sw = surface.get_width()
        sh = surface.get_height()
        sly, slx = region._slices
        (np.frombuffer(surface.get_data(), np.uint32)
         .reshape((sh, sw))[sly, slx]) = region._data
        surface.mark_dirty_rectangle(
            slx.start, sly.start, slx.stop - slx.start, sly.stop - sly.start)
