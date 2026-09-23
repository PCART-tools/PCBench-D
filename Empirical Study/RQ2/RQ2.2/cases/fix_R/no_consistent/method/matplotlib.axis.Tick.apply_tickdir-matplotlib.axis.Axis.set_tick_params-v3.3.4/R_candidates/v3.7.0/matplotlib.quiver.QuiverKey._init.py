    def _init(self):
        if True:  # self._dpi_at_last_init != self.axes.figure.dpi
            if self.Q._dpi_at_last_init != self.Q.axes.figure.dpi:
                self.Q._init()
            self._set_transform()
            with cbook._setattr_cm(self.Q, pivot=self.pivot[self.labelpos],
                                   # Hack: save and restore the Umask
                                   Umask=ma.nomask):
                u = self.U * np.cos(np.radians(self.angle))
                v = self.U * np.sin(np.radians(self.angle))
                angle = (self.Q.angles if isinstance(self.Q.angles, str)
                         else 'uv')
                self.verts = self.Q._make_verts(
                    np.array([u]), np.array([v]), angle)
            kwargs = self.Q.polykw
            kwargs.update(self.kw)
            self.vector = mcollections.PolyCollection(
                self.verts,
                offsets=[(self.X, self.Y)],
                offset_transform=self.get_transform(),
                **kwargs)
            if self.color is not None:
                self.vector.set_color(self.color)
            self.vector.set_transform(self.Q.get_transform())
            self.vector.set_figure(self.get_figure())
            self._dpi_at_last_init = self.Q.axes.figure.dpi
