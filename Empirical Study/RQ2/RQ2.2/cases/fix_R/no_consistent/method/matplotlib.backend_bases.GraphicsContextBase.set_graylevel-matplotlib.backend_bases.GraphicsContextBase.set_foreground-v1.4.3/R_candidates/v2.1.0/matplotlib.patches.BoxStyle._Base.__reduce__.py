        def __reduce__(self):
            # because we have decided to nest thes classes, we need to
            # add some more information to allow instance pickling.
            import matplotlib.cbook as cbook
            return (cbook._NestedClassGetter(),
                    (BoxStyle, self.__class__.__name__),
                    self.__dict__
                    )
