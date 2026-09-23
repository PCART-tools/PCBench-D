    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        # Object feature encoding
        self.visn_fc = tf.keras.layers.Dense(
            config.hidden_size,
            kernel_initializer=get_initializer(config.initializer_range),
            name="visn_fc",
        )
        self.visn_layer_norm = tf.keras.layers.LayerNormalization(
            epsilon=config.layer_norm_eps, name="visn_layer_norm"
        )

        # Box position encoding
        self.box_fc = tf.keras.layers.Dense(
            config.hidden_size,
            kernel_initializer=get_initializer(config.initializer_range),
            name="box_fc",
        )
        self.box_layer_norm = tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_eps, name="box_layer_norm")

        self.dropout = tf.keras.layers.Dropout(config.hidden_dropout_prob)
