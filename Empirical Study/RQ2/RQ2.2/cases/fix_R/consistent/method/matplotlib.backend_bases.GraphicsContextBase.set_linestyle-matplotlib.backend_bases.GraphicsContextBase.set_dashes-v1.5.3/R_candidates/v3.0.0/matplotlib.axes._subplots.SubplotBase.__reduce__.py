    def __reduce__(self):
        # get the first axes class which does not inherit from a subplotbase
        axes_class = next(
            c for c in type(self).__mro__
            if issubclass(c, Axes) and not issubclass(c, SubplotBase))
        return (_picklable_subplot_class_constructor,
                (axes_class,),
                self.__getstate__())
