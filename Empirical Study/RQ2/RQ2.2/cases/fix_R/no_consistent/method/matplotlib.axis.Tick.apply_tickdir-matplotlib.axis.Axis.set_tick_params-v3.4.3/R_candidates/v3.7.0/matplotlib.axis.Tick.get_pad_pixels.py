    @_api.deprecated("3.6")
    def get_pad_pixels(self):
        return self.figure.dpi * self._base_pad / 72
