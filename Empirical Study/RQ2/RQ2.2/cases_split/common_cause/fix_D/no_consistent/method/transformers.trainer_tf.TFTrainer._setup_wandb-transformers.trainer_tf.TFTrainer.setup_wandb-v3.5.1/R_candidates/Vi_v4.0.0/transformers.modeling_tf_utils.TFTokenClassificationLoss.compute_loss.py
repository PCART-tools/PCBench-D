    def compute_loss(self, labels, logits):
        loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=True, reduction=tf.keras.losses.Reduction.NONE
        )
        # make sure only labels that are not equal to -100
        # are taken into account as loss
        if tf.math.reduce_any(labels == -1):
            warnings.warn("Using `-1` to mask the loss for the token is deprecated. Please use `-100` instead.")
            active_loss = tf.reshape(labels, (-1,)) != -1
        else:
            active_loss = tf.reshape(labels, (-1,)) != -100
        reduced_logits = tf.boolean_mask(tf.reshape(logits, (-1, shape_list(logits)[2])), active_loss)
        labels = tf.boolean_mask(tf.reshape(labels, (-1,)), active_loss)

        return loss_fn(labels, reduced_logits)
