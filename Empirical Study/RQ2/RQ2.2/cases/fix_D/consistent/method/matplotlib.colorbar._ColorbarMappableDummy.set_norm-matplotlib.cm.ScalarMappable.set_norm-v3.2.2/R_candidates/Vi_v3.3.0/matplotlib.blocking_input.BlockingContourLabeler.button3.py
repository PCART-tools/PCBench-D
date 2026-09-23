    def button3(self, event):
        """
        Process an button-3 event (remove a label if not in inline mode).

        Unfortunately, if one is doing inline labels, then there is currently
        no way to fix the broken contour - once humpty-dumpty is broken, he
        can't be put back together.  In inline mode, this does nothing.

        Parameters
        ----------
        event : `~.backend_bases.MouseEvent`
        """
        if self.inline:
            pass
        else:
            self.cs.pop_label()
            self.cs.ax.figure.canvas.draw()
