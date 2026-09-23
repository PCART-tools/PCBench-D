    def __reduce__(self):
        # get the first axes class which does not
        # inherit from a subplotbase

        def not_subplotbase(c):
            return issubclass(c, Axes) and not issubclass(c, SubplotBase)

        axes_class = [c for c in self.__class__.mro()
                      if not_subplotbase(c)][0]
        r = [_PicklableSubplotClassConstructor(),
             (axes_class,),
             self.__getstate__()]
        return tuple(r)
