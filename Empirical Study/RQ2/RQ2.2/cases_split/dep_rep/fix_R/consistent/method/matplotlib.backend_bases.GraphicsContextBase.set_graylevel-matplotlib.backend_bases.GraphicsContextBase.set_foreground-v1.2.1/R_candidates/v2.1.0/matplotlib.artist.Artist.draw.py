    def draw(self, renderer, *args, **kwargs):
        'Derived classes drawing method'
        if not self.get_visible():
            return
        self.stale = False
