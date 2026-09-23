    def __init__(self, config, n_labels, **kwargs):
        super().__init__(**kwargs)
        initializer = get_initializer(config.initializer_range)
        self.linear_hidden = tf.keras.layers.Dense(
            config.d_model, kernel_initializer=initializer, name="linear_hidden"
        )
        self.dropout = tf.keras.layers.Dropout(config.hidden_dropout)
        self.linear_out = tf.keras.layers.Dense(n_labels, kernel_initializer=initializer, name="linear_out")
