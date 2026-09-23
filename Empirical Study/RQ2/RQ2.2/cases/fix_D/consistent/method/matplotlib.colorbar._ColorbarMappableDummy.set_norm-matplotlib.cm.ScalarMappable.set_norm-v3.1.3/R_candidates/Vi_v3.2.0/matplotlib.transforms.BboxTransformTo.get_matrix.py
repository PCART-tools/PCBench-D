    def get_matrix(self):
        # docstring inherited
        if self._invalid:
            outl, outb, outw, outh = self._boxout.bounds
            if DEBUG and (outw == 0 or outh == 0):
                raise ValueError("Transforming to a singular bounding box.")
            self._mtx = np.array([[outw,  0.0, outl],
                                  [ 0.0, outh, outb],
                                  [ 0.0,  0.0,  1.0]],
                                  float)
            self._inverted = None
            self._invalid = 0
        return self._mtx
