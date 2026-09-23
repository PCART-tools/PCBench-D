    def buffer_rgba(self):
        '''Get the image as an RGBA byte string.

        `draw` must be called at least once before this function will work and
        to update the renderer for any subsequent changes to the Figure.

        Returns
        -------
        bytes
        '''
        return self.renderer.buffer_rgba()
