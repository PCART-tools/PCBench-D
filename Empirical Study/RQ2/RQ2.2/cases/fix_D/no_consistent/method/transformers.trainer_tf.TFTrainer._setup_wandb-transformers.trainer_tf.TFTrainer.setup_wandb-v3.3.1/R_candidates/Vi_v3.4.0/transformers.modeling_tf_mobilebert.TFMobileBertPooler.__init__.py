    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.do_activate = config.classifier_activation
        if self.do_activate:
            self.dense = tf.keras.layers.Dense(
                config.hidden_size,
                kernel_initializer=get_initializer(config.initializer_range),
                activation="tanh",
                name="dense",
            )
