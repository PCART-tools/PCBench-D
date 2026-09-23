    @_api.deprecated("3.3")
    def funcbottom(self, val):
        self.targetfig.subplots_adjust(bottom=val)
        if self.drawon:
            self.targetfig.canvas.draw()
