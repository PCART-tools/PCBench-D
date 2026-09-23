    @property
    def labelsep(self):
        return self._labelsep_inches * self.Q.axes.get_figure(root=True).dpi
