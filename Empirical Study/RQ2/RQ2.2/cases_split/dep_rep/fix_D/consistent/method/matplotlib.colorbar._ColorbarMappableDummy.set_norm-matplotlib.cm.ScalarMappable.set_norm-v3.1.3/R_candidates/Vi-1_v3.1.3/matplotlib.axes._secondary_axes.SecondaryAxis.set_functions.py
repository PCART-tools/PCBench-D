    def set_functions(self, functions):
        """
        Set how the secondary axis converts limits from the parent axes.

        Parameters
        ----------
        functions : 2-tuple of func, or `Transform` with an inverse.
            Transform between the parent axis values and the secondary axis
            values.

            If supplied as a 2-tuple of functions, the first function is
            the forward transform function and the second is the inverse
            transform.

            If a transform is supplied, then the transform must have an
            inverse.

        """

        if self._orientation == 'x':
            set_scale = self.set_xscale
            parent_scale = self._parent.get_xscale()
        else:
            set_scale = self.set_yscale
            parent_scale = self._parent.get_yscale()
        # we need to use a modified scale so the scale can receive the
        # transform.  Only types supported are linear and log10 for now.
        # Probably possible to add other transforms as a todo...
        if parent_scale == 'log':
            defscale = 'functionlog'
        else:
            defscale = 'function'

        if (isinstance(functions, tuple) and len(functions) == 2 and
            callable(functions[0]) and callable(functions[1])):
            # make an arbitrary convert from a two-tuple of functions
            # forward and inverse.
            self._functions = functions
        elif functions is None:
            self._functions = (lambda x: x, lambda x: x)
        else:
            raise ValueError('functions argument of secondary axes '
                             'must be a two-tuple of callable functions '
                             'with the first function being the transform '
                             'and the second being the inverse')
        # need to invert the roles here for the ticks to line up.
        set_scale(defscale, functions=self._functions[::-1])
