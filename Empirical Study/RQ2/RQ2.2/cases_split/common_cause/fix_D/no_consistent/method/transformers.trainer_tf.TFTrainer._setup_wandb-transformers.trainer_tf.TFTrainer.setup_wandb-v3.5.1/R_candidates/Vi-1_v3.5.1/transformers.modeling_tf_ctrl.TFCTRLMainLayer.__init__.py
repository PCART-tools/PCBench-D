    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.output_hidden_states = config.output_hidden_states
        self.output_attentions = config.output_attentions
        self.use_cache = config.use_cache
        self.return_dict = config.use_return_dict

        self.d_model_size = config.n_embd
        self.num_layers = config.n_layer

        self.pos_encoding = positional_encoding(config.n_positions, self.d_model_size)

        self.w = TFSharedEmbeddings(
            config.vocab_size, config.n_embd, initializer_range=config.initializer_range, name="w"
        )

        self.dropout = tf.keras.layers.Dropout(config.embd_pdrop)
        self.h = [
            TFEncoderLayer(
                config.n_embd,
                config.n_head,
                config.dff,
                config.resid_pdrop,
                config.layer_norm_epsilon,
                self.output_attentions,
                name="h_._{}".format(i),
            )
            for i in range(config.n_layer)
        ]
        self.layernorm = tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_epsilon, name="layernorm")
