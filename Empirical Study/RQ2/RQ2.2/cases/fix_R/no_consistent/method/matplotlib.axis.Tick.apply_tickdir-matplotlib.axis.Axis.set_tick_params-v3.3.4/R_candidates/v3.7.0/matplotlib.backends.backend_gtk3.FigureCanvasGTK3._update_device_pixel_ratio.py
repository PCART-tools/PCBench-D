    def _update_device_pixel_ratio(self, *args, **kwargs):
        # We need to be careful in cases with mixed resolution displays if
        # device_pixel_ratio changes.
        if self._set_device_pixel_ratio(self.get_scale_factor()):
            # The easiest way to resize the canvas is to emit a resize event
            # since we implement all the logic for resizing the canvas for that
            # event.
            self.queue_resize()
            self.queue_draw()
