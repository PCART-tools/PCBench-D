    def get_edgecolor(self):
        if cbook._str_equal(self._edgecolors, 'face'):
            return self.get_facecolors()
        else:
            return self._edgecolors
