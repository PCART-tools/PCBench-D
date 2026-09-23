    @cbook.deprecated("3.3")
    def funcleft(self, val):
        self.targetfig.subplots_adjust(left=val)
        if self.drawon:
            self.targetfig.canvas.draw()
