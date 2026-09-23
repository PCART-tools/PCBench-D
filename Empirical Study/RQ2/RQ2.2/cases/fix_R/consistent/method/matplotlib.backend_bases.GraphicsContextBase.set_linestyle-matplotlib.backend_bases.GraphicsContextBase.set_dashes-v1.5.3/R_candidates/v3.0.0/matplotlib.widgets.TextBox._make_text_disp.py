    def _make_text_disp(self, string):
        return self.ax.text(self.DIST_FROM_LEFT, 0.5, string,
                            verticalalignment='center',
                            horizontalalignment='left',
                            transform=self.ax.transAxes)
