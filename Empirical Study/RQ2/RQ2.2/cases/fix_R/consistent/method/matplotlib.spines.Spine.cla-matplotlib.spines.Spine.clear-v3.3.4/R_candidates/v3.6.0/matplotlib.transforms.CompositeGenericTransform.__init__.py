    def __init__(self, a, b, **kwargs):
        """
        Create a new composite transform that is the result of
        applying transform *a* then transform *b*.

        You will generally not call this constructor directly but write ``a +
        b`` instead, which will automatically choose the best kind of composite
        transform instance to create.
        """
        if a.output_dims != b.input_dims:
            raise ValueError("The output dimension of 'a' must be equal to "
                             "the input dimensions of 'b'")
        self.input_dims = a.input_dims
        self.output_dims = b.output_dims

        super().__init__(**kwargs)
        self._a = a
        self._b = b
        self.set_children(a, b)
