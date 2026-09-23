    def _update_transScale(self):
        self.transScale.set(
            mtransforms.blended_transform_factory(
                self.xaxis.get_transform(), self.yaxis.get_transform()))
        for line in getattr(self, "_children", []):  # Not set during init.
            if not isinstance(line, mlines.Line2D):
                continue
            try:
                line._transformed_path.invalidate()
            except AttributeError:
                pass
