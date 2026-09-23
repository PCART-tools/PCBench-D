    def get_size(self):
        """Get the numrows, numcols of the input image"""
        if self._A is None:
            raise RuntimeError('You must first set the image array')

        return self._A.shape[:2]
