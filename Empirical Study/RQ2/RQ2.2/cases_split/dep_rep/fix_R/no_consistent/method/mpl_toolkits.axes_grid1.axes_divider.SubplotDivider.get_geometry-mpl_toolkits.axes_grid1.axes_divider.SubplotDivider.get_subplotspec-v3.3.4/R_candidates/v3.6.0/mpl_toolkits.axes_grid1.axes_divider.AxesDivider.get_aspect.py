    def get_aspect(self):
        if self._aspect is None:
            aspect = self._axes.get_aspect()
            if aspect == "auto":
                return False
            else:
                return True
        else:
            return self._aspect
