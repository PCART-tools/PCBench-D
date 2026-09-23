    def __setstate__(self, state):
        # re-initialise the TransformWrapper with the state's child
        self._init(state['child'])
        # The child may not be unpickled yet, so restore its information.
        self.input_dims = state['input_dims']
        self.output_dims = state['output_dims']
        # turn the normal dictionary back into a dictionary with weak
        # values
        self._parents = dict((k, weakref.ref(v)) for (k, v) in
                             six.iteritems(state['parents']) if v is not None)
