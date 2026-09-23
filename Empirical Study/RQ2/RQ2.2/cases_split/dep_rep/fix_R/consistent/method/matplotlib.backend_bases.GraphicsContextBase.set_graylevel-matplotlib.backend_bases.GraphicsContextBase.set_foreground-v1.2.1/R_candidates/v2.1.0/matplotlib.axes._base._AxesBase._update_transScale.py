    def _update_transScale(self):
        self.transScale.set(
            mtransforms.blended_transform_factory(
                self.xaxis.get_transform(), self.yaxis.get_transform()))
        if hasattr(self, "lines"):
            for line in self.lines:
                try:
                    line._transformed_path.invalidate()
                except AttributeError:
                    pass
