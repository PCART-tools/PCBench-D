def _picklable_subplot_class_constructor(axes_class):
    """
    Stub factory that returns an empty instance of the appropriate subplot
    class when called with an axes class. This is purely to allow pickling of
    Axes and Subplots.
    """
    subplot_class = subplot_class_factory(axes_class)
    return subplot_class.__new__(subplot_class)
