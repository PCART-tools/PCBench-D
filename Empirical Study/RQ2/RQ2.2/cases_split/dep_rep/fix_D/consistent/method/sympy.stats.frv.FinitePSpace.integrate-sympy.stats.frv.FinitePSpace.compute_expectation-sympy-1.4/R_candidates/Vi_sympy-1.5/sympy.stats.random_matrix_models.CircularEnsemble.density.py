    def density(self, expr):
        # TODO : Add support for Lie groups(as extensions of sympy.diffgeom)
        #        and define measures on them
        raise NotImplementedError("Support for Haar measure hasn't been "
                                  "implemented yet, therefore the density of "
                                  "%s cannot be computed."%(self))
