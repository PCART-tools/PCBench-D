    def run_model(self, features, labels, training):
        """
        Computes the loss of the given features and labels pair.

        Subclass and override this method if you want to inject some custom behavior.

        Args:
            features (:obj:`tf.Tensor`): A batch of input features.
            labels (:obj:`tf.Tensor`): A batch of labels.
            training (:obj:`bool`): Whether or not to run the model in training mode.

        Returns:
            A tuple of two :obj:`tf.Tensor`: The loss and logits.
        """
        if hasattr(self, "_run_model"):
            warnings.warn(
                "The `_run_model` method is deprecated and won't be called in a future version, define `run_model` in your subclass.",
                FutureWarning,
            )
            return self._run_model(features, labels, training)

        if self.args.past_index >= 0 and getattr(self, "_past", None) is not None:
            features["mems"] = self._past

        if isinstance(labels, (dict)):
            outputs = self.model(features, training=training, **labels)[:2]
        else:
            outputs = self.model(features, labels=labels, training=training)[:2]

        loss, logits = outputs[:2]

        if self.args.past_index >= 0:
            self._past = outputs[self.args.past_index]

        return loss, logits
