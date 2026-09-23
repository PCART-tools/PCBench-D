        def invalidate(self):
            self._check(self._points)
            TransformNode.invalidate(self)
