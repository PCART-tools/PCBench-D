        class ClaSuperAxes(Axes):
            def cla(self):
                nonlocal called
                called = True
                super().cla()
