    def set_filternorm(self, filternorm):
        """
        Set whether the resize filter norms the weights -- see
        help for imshow

        ACCEPTS: 0 or 1
        """
        if filternorm:
            self._filternorm = 1
        else:
            self._filternorm = 0

        self.stale = True
