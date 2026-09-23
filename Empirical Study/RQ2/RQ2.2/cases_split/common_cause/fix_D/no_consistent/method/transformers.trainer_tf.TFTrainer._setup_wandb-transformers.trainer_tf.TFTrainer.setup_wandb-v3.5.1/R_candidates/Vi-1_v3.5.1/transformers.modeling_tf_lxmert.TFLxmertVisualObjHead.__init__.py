    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.transform = TFLxmertPredictionHeadTransform(config, name="transform")

        # Decide the use of visual losses
        visual_losses = {}
        if config.visual_obj_loss:
            visual_losses["obj"] = {"shape": (-1,), "num": config.num_object_labels}
        if config.visual_attr_loss:
            visual_losses["attr"] = {"shape": (-1,), "num": config.num_attr_labels}
        if config.visual_obj_loss:
            visual_losses["feat"] = {"shape": (-1, 2048), "num": config.visual_feat_dim}
        self.visual_losses = visual_losses

        # The output weights are the same as the input embeddings, but there is
        # an output-only bias for each token.
        self.decoder_dict = {
            key: tf.keras.layers.Dense(
                self.visual_losses[key]["num"],
                kernel_initializer=get_initializer(config.initializer_range),
                name=f"decoder_dict.{key}",
            )
            for key in self.visual_losses
        }
