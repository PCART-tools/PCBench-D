    def build(self, input_shape):
        """Build shared word embedding layer """
        with tf.name_scope("word_embeddings"):
            # Create and initialize weights. The random normal initializer was chosen
            # arbitrarily, and works well.
            self.word_embeddings = self.add_weight(
                "weight",
                shape=[self.config.vocab_size, self.config.embedding_size],
                initializer=get_initializer(self.config.initializer_range),
            )
        super().build(input_shape)
