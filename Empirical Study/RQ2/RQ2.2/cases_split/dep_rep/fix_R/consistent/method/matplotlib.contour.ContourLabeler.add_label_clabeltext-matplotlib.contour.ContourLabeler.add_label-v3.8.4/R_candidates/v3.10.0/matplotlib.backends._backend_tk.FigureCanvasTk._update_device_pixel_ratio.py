    def _update_device_pixel_ratio(self, event=None):
        ratio = None
        if sys.platform == 'win32':
            # Tk gives scaling with respect to 72 DPI, but Windows screens are
            # scaled vs 96 dpi, and pixel ratio settings are given in whole
            # percentages, so round to 2 digits.
            ratio = round(self._tkcanvas.tk.call('tk', 'scaling') / (96 / 72), 2)
        elif sys.platform == "linux":
            ratio = self._tkcanvas.winfo_fpixels('1i') / 96
        if ratio is not None and self._set_device_pixel_ratio(ratio):
            # The easiest way to resize the canvas is to resize the canvas
            # widget itself, since we implement all the logic for resizing the
            # canvas backing store on that event.
            w, h = self.get_width_height(physical=True)
            self._tkcanvas.configure(width=w, height=h)
