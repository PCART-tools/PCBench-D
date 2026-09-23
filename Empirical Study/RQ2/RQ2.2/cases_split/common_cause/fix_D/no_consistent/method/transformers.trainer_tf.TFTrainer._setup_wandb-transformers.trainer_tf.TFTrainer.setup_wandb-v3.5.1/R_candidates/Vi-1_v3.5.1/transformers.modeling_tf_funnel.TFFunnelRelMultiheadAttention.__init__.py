    def __init__(self, config, block_index, **kwargs):
        super().__init__(**kwargs)
        self.attention_type = config.attention_type
        self.n_head = n_head = config.n_head
        self.d_head = d_head = config.d_head
        self.d_model = d_model = config.d_model
        self.initializer_range = config.initializer_range
        self.block_index = block_index

        self.hidden_dropout = tf.keras.layers.Dropout(config.hidden_dropout)
        self.attention_dropout = tf.keras.layers.Dropout(config.attention_dropout)

        initializer = get_initializer(config.initializer_range)

        self.q_head = tf.keras.layers.Dense(
            n_head * d_head, use_bias=False, kernel_initializer=initializer, name="q_head"
        )
        self.k_head = tf.keras.layers.Dense(n_head * d_head, kernel_initializer=initializer, name="k_head")
        self.v_head = tf.keras.layers.Dense(n_head * d_head, kernel_initializer=initializer, name="v_head")

        self.post_proj = tf.keras.layers.Dense(d_model, kernel_initializer=initializer, name="post_proj")
        self.layer_norm = tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_eps, name="layer_norm")
        self.scale = 1.0 / (d_head ** 0.5)
