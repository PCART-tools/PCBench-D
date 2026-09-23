    def get_subplotspec(self):
        if hasattr(self._axes, "get_subplotspec"):
            return self._axes.get_subplotspec()
        else:
            return None
