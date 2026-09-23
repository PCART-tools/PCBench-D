    class ClearAxes(Axes):
        def clear(self):
            nonlocal called
            called = True
