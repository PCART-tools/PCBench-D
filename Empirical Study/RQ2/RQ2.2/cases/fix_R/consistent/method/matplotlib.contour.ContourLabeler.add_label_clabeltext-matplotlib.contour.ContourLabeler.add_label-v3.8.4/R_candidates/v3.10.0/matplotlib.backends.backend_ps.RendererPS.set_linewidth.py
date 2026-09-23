    def set_linewidth(self, linewidth, store=True):
        linewidth = float(linewidth)
        if linewidth != self.linewidth:
            self._pswriter.write(f"{_nums_to_str(linewidth)} setlinewidth\n")
            if store:
                self.linewidth = linewidth
