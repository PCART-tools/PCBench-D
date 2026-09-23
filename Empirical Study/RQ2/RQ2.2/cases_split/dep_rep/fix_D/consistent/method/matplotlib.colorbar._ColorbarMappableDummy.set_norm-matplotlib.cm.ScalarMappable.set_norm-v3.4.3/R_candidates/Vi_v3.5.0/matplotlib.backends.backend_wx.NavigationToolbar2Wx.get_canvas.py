    @_api.deprecated("3.4")
    def get_canvas(self, frame, fig):
        return type(self.canvas)(frame, -1, fig)
