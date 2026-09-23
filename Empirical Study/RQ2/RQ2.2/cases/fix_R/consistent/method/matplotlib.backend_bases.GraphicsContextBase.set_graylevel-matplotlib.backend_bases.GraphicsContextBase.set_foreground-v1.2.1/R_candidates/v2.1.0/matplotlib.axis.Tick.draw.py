    @allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            self.stale = False
            return

        renderer.open_group(self.__name__)
        if self.gridOn:
            self.gridline.draw(renderer)
        if self.tick1On:
            self.tick1line.draw(renderer)
        if self.tick2On:
            self.tick2line.draw(renderer)

        if self.label1On:
            self.label1.draw(renderer)
        if self.label2On:
            self.label2.draw(renderer)
        renderer.close_group(self.__name__)

        self.stale = False
