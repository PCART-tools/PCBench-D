    @nn.compact
    def __call__(self, hidden_state):
        # TODO: Add ACT2FN reference to change activation function
        dense = nn.Dense(features=self.output_size, name="dense")(hidden_state)
        return gelu(dense)
