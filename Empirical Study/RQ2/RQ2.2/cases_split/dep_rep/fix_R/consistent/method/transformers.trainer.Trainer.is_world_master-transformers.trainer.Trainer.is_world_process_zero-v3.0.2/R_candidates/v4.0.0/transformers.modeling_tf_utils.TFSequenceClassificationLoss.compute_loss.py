    def compute_loss(self, labels, logits):
        if len(shape_list(logits)) == 1 or shape_list(logits)[1] == 1:
            loss_fn = tf.keras.losses.MeanSquaredError(reduction=tf.keras.losses.Reduction.NONE)
        else:
            loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(
                from_logits=True, reduction=tf.keras.losses.Reduction.NONE
            )

        return loss_fn(labels, logits)
