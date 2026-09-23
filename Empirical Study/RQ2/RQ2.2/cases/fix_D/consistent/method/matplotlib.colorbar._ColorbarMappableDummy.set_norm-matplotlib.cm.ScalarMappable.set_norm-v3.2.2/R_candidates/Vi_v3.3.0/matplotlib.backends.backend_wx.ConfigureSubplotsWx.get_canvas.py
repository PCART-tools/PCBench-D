    @cbook.deprecated("3.2")
    def get_canvas(self, frame, fig):
        return type(self.canvas)(frame, -1, fig)
