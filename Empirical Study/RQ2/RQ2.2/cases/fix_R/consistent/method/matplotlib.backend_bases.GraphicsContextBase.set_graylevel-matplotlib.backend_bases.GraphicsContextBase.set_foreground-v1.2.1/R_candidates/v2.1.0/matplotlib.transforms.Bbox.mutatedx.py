    def mutatedx(self):
        'return whether the x-limits have changed since init'
        return (self._points[0, 0] != self._points_orig[0, 0] or
                self._points[1, 0] != self._points_orig[1, 0])
