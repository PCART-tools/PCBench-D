    def __call__(self, axes_class):
        # create a dummy object instance
        subplot_instance = _PicklableSubplotClassConstructor()
        subplot_class = subplot_class_factory(axes_class)
        # update the class to the desired subplot class
        subplot_instance.__class__ = subplot_class
        return subplot_instance
