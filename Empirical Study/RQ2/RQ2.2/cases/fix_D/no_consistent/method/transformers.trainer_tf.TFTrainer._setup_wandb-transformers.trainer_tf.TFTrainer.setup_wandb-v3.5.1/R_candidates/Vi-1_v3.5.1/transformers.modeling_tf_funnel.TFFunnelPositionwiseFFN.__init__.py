    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        initializer = get_initializer(config.initializer_range)
        self.linear_1 = tf.keras.layers.Dense(config.d_inner, kernel_initializer=initializer, name="linear_1")
        self.activation_function = get_tf_activation(config.hidden_act)
        self.activation_dropout = tf.keras.layers.Dropout(config.activation_dropout)
        self.linear_2 = tf.keras.layers.Dense(config.d_model, kernel_initializer=initializer, name="linear_2")
        self.dropout = tf.keras.layers.Dropout(config.hidden_dropout)
        self.layer_norm = tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_eps, name="layer_norm")
