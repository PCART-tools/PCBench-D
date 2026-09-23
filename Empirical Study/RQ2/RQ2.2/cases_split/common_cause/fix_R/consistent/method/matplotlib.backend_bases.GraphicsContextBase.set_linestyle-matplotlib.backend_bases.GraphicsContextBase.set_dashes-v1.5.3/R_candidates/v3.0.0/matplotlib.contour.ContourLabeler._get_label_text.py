    def _get_label_text(self, x, y, rotation):
        dx, dy = self.ax.transData.inverted().transform_point((x, y))
        t = text.Text(dx, dy, rotation=rotation,
                      horizontalalignment='center',
                      verticalalignment='center')
        return t
