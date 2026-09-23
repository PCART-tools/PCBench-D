    def __init__(self, epsilon=1e-6, **kwargs):
        """Construct a layernorm module in the T5 style
        No bias and no substraction of mean.
        """
        super().__init__(**kwargs)
        self.variance_epsilon = epsilon
