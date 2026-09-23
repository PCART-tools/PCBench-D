    def button3(self, event):
        """
        This will be called if button 3 is clicked.  This will remove
        a label if not in inline mode.  Unfortunately, if one is doing
        inline labels, then there is currently no way to fix the
        broken contour - once humpty-dumpty is broken, he can't be put
        back together.  In inline mode, this does nothing.
        """

        if self.inline:
            pass
        else:
            self.cs.pop_label()
            self.cs.ax.figure.canvas.draw()
