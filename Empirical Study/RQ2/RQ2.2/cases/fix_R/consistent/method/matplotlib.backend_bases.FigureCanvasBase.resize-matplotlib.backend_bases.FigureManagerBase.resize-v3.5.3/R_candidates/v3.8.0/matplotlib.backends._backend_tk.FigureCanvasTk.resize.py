    def resize(self, event):
        width, height = event.width, event.height

        # compute desired figure size in inches
        dpival = self.figure.dpi
        winch = width / dpival
        hinch = height / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)

        self._tkcanvas.delete(self._tkcanvas_image_region)
        self._tkphoto.configure(width=int(width), height=int(height))
        self._tkcanvas_image_region = self._tkcanvas.create_image(
            int(width / 2), int(height / 2), image=self._tkphoto)
        ResizeEvent("resize_event", self)._process()
        self.draw_idle()
