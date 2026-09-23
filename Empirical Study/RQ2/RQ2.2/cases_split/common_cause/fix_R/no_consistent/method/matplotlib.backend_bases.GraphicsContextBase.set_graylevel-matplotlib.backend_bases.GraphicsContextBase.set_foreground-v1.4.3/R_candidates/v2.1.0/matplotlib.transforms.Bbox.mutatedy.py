    def mutatedy(self):
        'return whether the y-limits have changed since init'
        return (self._points[0, 1] != self._points_orig[0, 1] or
                self._points[1, 1] != self._points_orig[1, 1])
