    def draw(self, renderer):
        self._transformed_path = None  # Force regen.
        super().draw(renderer)
