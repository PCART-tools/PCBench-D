    def __getstate__(self):
        # only store the child information and parents
        return {
            'child': self._child,
            'input_dims': self.input_dims,
            'output_dims': self.output_dims,
            # turn the weak-values dictionary into a normal dictionary
            'parents': dict((k, v()) for (k, v) in
                            six.iteritems(self._parents))
        }
