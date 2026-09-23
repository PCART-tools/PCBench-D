    def get_subplotspec(self):
        if hasattr(self._axes_divider, "get_subplotspec"):
            return self._axes_divider.get_subplotspec()
        else:
            return None
