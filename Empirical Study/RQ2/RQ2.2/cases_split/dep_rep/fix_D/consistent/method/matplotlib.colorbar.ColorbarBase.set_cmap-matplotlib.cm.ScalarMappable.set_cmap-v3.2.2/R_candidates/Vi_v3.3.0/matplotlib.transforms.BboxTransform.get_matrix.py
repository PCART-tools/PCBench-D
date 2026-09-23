    def get_matrix(self):
        # docstring inherited
        if self._invalid:
            inl, inb, inw, inh = self._boxin.bounds
            outl, outb, outw, outh = self._boxout.bounds
            x_scale = outw / inw
            y_scale = outh / inh
            if DEBUG and (x_scale == 0 or y_scale == 0):
                raise ValueError(
                    "Transforming from or to a singular bounding box")
            self._mtx = np.array([[x_scale, 0.0    , (-inl*x_scale+outl)],
                                  [0.0    , y_scale, (-inb*y_scale+outb)],
                                  [0.0    , 0.0    , 1.0        ]],
                                 float)
            self._inverted = None
            self._invalid = 0
        return self._mtx
