    @compact
    def __call__(self, hidden_state):
        cls_token = hidden_state[:, 0]
        out = nn.Dense(hidden_state.shape[-1], name="dense")(cls_token)
        return jax.lax.tanh(out)
