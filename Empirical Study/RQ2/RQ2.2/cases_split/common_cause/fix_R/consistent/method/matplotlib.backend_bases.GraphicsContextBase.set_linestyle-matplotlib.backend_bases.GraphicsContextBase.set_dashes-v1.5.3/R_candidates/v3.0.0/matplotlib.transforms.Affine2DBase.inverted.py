    def inverted(self):
        if self._inverted is None or self._invalid:
            mtx = self.get_matrix()
            shorthand_name = None
            if self._shorthand_name:
                shorthand_name = '(%s)-1' % self._shorthand_name
            self._inverted = Affine2D(inv(mtx), shorthand_name=shorthand_name)
            self._invalid = 0
        return self._inverted
