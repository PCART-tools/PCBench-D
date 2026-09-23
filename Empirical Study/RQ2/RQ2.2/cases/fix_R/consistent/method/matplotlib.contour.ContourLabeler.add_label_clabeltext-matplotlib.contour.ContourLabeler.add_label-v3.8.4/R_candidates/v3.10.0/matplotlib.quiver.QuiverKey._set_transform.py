    def _set_transform(self):
        fig = self.Q.axes.get_figure(root=False)
        self.set_transform(_api.check_getitem({
            "data": self.Q.axes.transData,
            "axes": self.Q.axes.transAxes,
            "figure": fig.transFigure,
            "inches": fig.dpi_scale_trans,
        }, coordinates=self.coord))
