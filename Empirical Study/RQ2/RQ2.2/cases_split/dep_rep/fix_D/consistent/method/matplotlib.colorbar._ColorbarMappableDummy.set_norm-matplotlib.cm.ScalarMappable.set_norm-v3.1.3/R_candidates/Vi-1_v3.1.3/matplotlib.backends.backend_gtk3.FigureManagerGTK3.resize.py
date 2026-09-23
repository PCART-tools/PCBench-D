    def resize(self, width, height):
        'set the canvas size in pixels'
        #_, _, cw, ch = self.canvas.allocation
        #_, _, ww, wh = self.window.allocation
        #self.window.resize (width-cw+ww, height-ch+wh)
        self.window.resize(width, height)
