    @property
    def dummy_inputs(self):
        input_ids = tf.constant([[7, 6, 0, 0, 1], [1, 2, 3, 0, 0], [0, 0, 0, 4, 5]])
        # make sure global layers are initialized
        attention_mask = tf.constant([[1, 1, 0, 0, 1], [1, 1, 1, 0, 0], [1, 0, 0, 1, 1]])
        global_attention_mask = tf.constant([[0, 0, 0, 0, 1], [0, 0, 1, 0, 0], [0, 0, 0, 0, 1]])
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "global_attention_mask": global_attention_mask,
        }
