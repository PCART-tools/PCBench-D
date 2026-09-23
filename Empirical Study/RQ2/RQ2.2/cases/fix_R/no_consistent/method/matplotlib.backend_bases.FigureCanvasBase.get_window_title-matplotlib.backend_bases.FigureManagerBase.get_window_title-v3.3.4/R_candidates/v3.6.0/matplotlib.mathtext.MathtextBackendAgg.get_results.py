    def get_results(self, box):
        self.image = None
        self.mode = 'render'
        return _mathtext.ship(box).to_raster()
