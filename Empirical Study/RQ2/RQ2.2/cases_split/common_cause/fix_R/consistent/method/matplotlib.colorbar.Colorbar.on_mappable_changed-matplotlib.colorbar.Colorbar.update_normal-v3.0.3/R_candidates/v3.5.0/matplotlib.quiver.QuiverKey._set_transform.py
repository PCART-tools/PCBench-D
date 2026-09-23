    def _set_transform(self):
        self.set_transform(_api.check_getitem({
            "data": self.Q.axes.transData,
            "axes": self.Q.axes.transAxes,
            "figure": self.Q.axes.figure.transFigure,
            "inches": self.Q.axes.figure.dpi_scale_trans,
        }, coordinates=self.coord))
