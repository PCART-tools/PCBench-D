    def set_canvas_size(self, w, h, d):
        """
        Set the size of the buffer used to render the math expression.
        Only really necessary for the bitmap backends.
        """
        self.width, self.height, self.depth = np.ceil([w, h, d])
        self.mathtext_backend.set_canvas_size(
            self.width, self.height, self.depth)
