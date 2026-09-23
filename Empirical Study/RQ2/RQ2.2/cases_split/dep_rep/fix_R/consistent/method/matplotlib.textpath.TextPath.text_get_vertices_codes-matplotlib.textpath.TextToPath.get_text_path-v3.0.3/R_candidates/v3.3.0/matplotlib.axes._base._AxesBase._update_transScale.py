    def _update_transScale(self):
        self.transScale.set(
            mtransforms.blended_transform_factory(
                self.xaxis.get_transform(), self.yaxis.get_transform()))
        for line in getattr(self, "lines", []):  # Not set during init.
            try:
                line._transformed_path.invalidate()
            except AttributeError:
                pass
