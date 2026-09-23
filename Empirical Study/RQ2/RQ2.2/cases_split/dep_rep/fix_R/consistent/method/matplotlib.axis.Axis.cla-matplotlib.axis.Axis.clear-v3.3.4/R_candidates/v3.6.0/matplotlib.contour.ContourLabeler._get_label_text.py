    def _get_label_text(self, x, y, rotation):
        dx, dy = self.axes.transData.inverted().transform((x, y))
        t = text.Text(dx, dy, rotation=rotation,
                      horizontalalignment='center',
                      verticalalignment='center', zorder=self._clabel_zorder)
        return t
