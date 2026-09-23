    def get_images(self):
        r"""Return a list of `.AxesImage`\s contained by the Axes."""
        return cbook.silent_list('AxesImage', self.images)
