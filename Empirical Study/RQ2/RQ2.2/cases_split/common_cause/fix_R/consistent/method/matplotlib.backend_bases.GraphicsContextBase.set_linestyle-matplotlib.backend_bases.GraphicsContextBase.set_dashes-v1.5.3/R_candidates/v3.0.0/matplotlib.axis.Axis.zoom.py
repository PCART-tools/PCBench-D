    def zoom(self, direction):
        "Zoom in/out on axis; if *direction* is >0 zoom in, else zoom out"
        self.major.locator.zoom(direction)
