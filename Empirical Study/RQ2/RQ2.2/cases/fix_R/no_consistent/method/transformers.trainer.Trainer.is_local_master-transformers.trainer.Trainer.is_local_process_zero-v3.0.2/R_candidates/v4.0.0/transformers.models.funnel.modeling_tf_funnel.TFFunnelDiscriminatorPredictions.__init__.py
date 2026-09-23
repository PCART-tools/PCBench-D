    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        initializer = get_initializer(config.initializer_range)
        self.dense = tf.keras.layers.Dense(config.d_model, kernel_initializer=initializer, name="dense")
        self.activation_function = get_tf_activation(config.hidden_act)
        self.dense_prediction = tf.keras.layers.Dense(1, kernel_initializer=initializer, name="dense_prediction")
