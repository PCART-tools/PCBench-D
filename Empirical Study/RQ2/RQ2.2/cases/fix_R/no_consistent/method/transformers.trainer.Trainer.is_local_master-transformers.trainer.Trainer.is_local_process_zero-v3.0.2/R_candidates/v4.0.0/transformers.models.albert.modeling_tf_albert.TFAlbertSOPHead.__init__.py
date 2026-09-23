    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.dropout = tf.keras.layers.Dropout(config.classifier_dropout_prob)
        self.classifier = tf.keras.layers.Dense(
            config.num_labels,
            kernel_initializer=get_initializer(config.initializer_range),
            name="classifier",
        )
