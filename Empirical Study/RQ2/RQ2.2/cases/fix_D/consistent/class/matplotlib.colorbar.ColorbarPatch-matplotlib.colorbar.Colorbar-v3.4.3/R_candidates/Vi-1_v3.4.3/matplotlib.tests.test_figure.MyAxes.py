    class MyAxes(Axes):
        def __init__(self, *args, myclass=None, **kwargs):
            return Axes.__init__(self, *args, **kwargs)
