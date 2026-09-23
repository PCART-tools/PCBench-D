    def call(self, input_ids: tf.Tensor, use_cache=False):
        """Input is expected to be of size [bsz x seqlen]."""
        bsz, seq_len = shape_list(input_ids)[:2]

        if use_cache:
            positions = tf.fill((1, 1), seq_len - 1)
        else:
            # starts at 0, ends at 1-seq_len
            positions = tf.range(0, seq_len, delta=1, dtype=tf.int32, name="range")
        return super().call(positions + self.offset)  # super object is not callable for some reason
