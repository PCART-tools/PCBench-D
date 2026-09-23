    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.n_heads = config.n_heads
        self.dim = config.dim
        self.dropout = tf.keras.layers.Dropout(config.attention_dropout)
        self.output_attentions = config.output_attentions

        assert self.dim % self.n_heads == 0, f"Hidden size {self.dim} not dividable by number of heads {self.n_heads}"

        self.q_lin = tf.keras.layers.Dense(
            config.dim, kernel_initializer=get_initializer(config.initializer_range), name="q_lin"
        )
        self.k_lin = tf.keras.layers.Dense(
            config.dim, kernel_initializer=get_initializer(config.initializer_range), name="k_lin"
        )
        self.v_lin = tf.keras.layers.Dense(
            config.dim, kernel_initializer=get_initializer(config.initializer_range), name="v_lin"
        )
        self.out_lin = tf.keras.layers.Dense(
            config.dim, kernel_initializer=get_initializer(config.initializer_range), name="out_lin"
        )

        self.pruned_heads = set()
