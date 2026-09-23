    class ClearSuperAxes(Axes):
        def clear(self):
            nonlocal called
            called = True
            super().clear()
