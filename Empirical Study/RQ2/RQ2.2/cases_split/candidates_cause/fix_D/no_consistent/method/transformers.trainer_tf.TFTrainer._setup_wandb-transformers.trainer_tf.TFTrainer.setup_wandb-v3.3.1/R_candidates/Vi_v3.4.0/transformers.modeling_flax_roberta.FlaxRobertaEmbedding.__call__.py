    @compact
    def __call__(self, inputs):
        embedding = self.param("weight", self.emb_init, (self.vocab_size, self.hidden_size))
        return jnp.take(embedding, inputs, axis=0)
