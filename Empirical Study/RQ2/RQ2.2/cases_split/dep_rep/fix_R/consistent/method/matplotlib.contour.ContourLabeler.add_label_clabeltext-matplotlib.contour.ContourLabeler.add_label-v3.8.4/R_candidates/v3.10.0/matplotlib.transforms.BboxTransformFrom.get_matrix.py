    def get_matrix(self):
        # docstring inherited
        if self._invalid:
            inl, inb, inw, inh = self._boxin.bounds
            if DEBUG and (inw == 0 or inh == 0):
                raise ValueError("Transforming from a singular bounding box.")
            x_scale = 1.0 / inw
            y_scale = 1.0 / inh
            self._mtx = np.array([[x_scale,     0.0, -inl*x_scale],
                                  [    0.0, y_scale, -inb*y_scale],
                                  [    0.0,     0.0,          1.0]],
                                 float)
            self._inverted = None
            self._invalid = 0
        return self._mtx
