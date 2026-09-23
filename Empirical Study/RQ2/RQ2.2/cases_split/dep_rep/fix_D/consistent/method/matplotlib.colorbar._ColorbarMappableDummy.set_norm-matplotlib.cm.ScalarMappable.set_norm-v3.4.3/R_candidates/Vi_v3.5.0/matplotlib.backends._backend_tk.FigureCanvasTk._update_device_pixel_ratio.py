    def _update_device_pixel_ratio(self, event=None):
        # Tk gives scaling with respect to 72 DPI, but most (all?) screens are
        # scaled vs 96 dpi, and pixel ratio settings are given in whole
        # percentages, so round to 2 digits.
        ratio = round(self._tkcanvas.tk.call('tk', 'scaling') / (96 / 72), 2)
        if self._set_device_pixel_ratio(ratio):
            # The easiest way to resize the canvas is to resize the canvas
            # widget itself, since we implement all the logic for resizing the
            # canvas backing store on that event.
            w, h = self.get_width_height(physical=True)
            self._tkcanvas.configure(width=w, height=h)
