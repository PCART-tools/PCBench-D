    def draw(self, renderer):
        if not self.get_visible() or not self._check_xy(renderer):
            return
        super().draw(renderer)
