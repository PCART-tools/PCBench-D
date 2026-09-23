    def __init__(self, config, num_labels, **kwargs):
        super().__init__(**kwargs)
        hid_dim = config.hidden_size
        self.dense = tf.keras.layers.Dense(
            hid_dim * 2,
            kernel_initializer=get_initializer(config.initializer_range),
            name="logit_fc_._0",
        )
        self.activation = get_tf_activation("gelu")
        self.layer_norm = tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_eps, name="logit_fc_._2")
        self.dense_1 = tf.keras.layers.Dense(
            num_labels,
            kernel_initializer=get_initializer(config.initializer_range),
            name="logit_fc_._3",
        )
