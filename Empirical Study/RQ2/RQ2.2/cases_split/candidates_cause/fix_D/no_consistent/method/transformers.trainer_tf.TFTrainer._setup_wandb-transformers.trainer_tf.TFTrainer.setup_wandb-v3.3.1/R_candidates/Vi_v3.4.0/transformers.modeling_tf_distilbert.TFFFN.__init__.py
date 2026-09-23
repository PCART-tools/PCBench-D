    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.dropout = tf.keras.layers.Dropout(config.dropout)
        self.lin1 = tf.keras.layers.Dense(
            config.hidden_dim, kernel_initializer=get_initializer(config.initializer_range), name="lin1"
        )
        self.lin2 = tf.keras.layers.Dense(
            config.dim, kernel_initializer=get_initializer(config.initializer_range), name="lin2"
        )
        assert config.activation in ["relu", "gelu"], "activation ({}) must be in ['relu', 'gelu']".format(
            config.activation
        )
        self.activation = get_tf_activation(config.activation)
