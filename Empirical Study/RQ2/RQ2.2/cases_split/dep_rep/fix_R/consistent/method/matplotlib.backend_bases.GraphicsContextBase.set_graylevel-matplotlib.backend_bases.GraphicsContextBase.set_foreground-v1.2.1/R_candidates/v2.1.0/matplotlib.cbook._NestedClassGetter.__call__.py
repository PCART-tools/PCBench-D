    def __call__(self, containing_class, class_name):
        nested_class = getattr(containing_class, class_name)

        # make an instance of a simple object (this one will do), for which we
        # can change the __class__ later on.
        nested_instance = _NestedClassGetter()

        # set the class of the instance, the __init__ will never be called on
        # the class but the original state will be set later on by pickle.
        nested_instance.__class__ = nested_class
        return nested_instance
