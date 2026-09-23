    def set_linewidth(self, linewidth, store=True):
        linewidth = float(linewidth)
        if linewidth != self.linewidth:
            self._pswriter.write("%1.3f setlinewidth\n" % linewidth)
            if store:
                self.linewidth = linewidth
