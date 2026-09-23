    @martist.allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            self.stale = False
            return
        renderer.open_group(self.__name__)
        for artist in [self.gridline, self.tick1line, self.tick2line,
                       self.label1, self.label2]:
            artist.draw(renderer)
        renderer.close_group(self.__name__)
        self.stale = False
