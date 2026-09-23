    def configure_event(self, widget, event):
        if widget.get_property("window") is None:
            return
        w = event.width * self.device_pixel_ratio
        h = event.height * self.device_pixel_ratio
        if w < 3 or h < 3:
            return  # empty fig
        # resize the figure (in inches)
        dpi = self.figure.dpi
        self.figure.set_size_inches(w / dpi, h / dpi, forward=False)
        return False  # finish event propagation?
