    @cbook.deprecated("3.3")
    @property
    def ctx(self):
        return self.canvas.get_property("window").cairo_create()
