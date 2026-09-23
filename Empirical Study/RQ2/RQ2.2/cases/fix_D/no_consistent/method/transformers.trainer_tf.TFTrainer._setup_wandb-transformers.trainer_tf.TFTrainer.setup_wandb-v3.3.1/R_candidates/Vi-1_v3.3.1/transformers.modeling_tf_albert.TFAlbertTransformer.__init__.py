    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.config = config
        self.embedding_hidden_mapping_in = tf.keras.layers.Dense(
            config.hidden_size,
            kernel_initializer=get_initializer(config.initializer_range),
            name="embedding_hidden_mapping_in",
        )
        self.albert_layer_groups = [
            TFAlbertLayerGroup(config, name="albert_layer_groups_._{}".format(i))
            for i in range(config.num_hidden_groups)
        ]
