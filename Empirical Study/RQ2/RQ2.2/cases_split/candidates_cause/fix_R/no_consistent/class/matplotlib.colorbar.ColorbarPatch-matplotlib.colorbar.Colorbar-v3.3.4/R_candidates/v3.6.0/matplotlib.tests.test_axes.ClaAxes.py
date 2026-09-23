        class ClaAxes(Axes):
            def cla(self):
                nonlocal called
                called = True
