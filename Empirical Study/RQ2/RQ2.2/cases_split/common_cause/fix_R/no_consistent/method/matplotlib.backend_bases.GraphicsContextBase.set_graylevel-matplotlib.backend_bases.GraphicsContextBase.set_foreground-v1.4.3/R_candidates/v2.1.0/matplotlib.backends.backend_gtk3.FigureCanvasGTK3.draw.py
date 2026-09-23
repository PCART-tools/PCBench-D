    def draw(self):
        if self.get_visible() and self.get_mapped():
            self.queue_draw()
            # do a synchronous draw (its less efficient than an async draw,
            # but is required if/when animation is used)
            self.get_property("window").process_updates (False)
