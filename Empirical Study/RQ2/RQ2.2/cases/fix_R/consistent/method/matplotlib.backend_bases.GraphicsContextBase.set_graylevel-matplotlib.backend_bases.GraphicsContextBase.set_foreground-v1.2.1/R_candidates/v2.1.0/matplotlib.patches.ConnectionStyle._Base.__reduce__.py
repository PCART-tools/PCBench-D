        def __reduce__(self):
            # because we have decided to nest these classes, we need to
            # add some more information to allow instance pickling.
            import matplotlib.cbook as cbook
            return (cbook._NestedClassGetter(),
                    (ConnectionStyle, self.__class__.__name__),
                    self.__dict__
                    )
