    def compute_bias(self, qlen, klen):
        """ Compute binned relative position bias """
        context_position = tf.range(qlen)[:, None]
        memory_position = tf.range(klen)[None, :]
        relative_position = memory_position - context_position  # shape (qlen, klen)
        rp_bucket = self._relative_position_bucket(
            relative_position,
            bidirectional=self.is_bidirectional,
            num_buckets=self.relative_attention_num_buckets,
        )
        values = self.relative_attention_bias(rp_bucket)  # shape (qlen, klen, num_heads)
        values = tf.expand_dims(tf.transpose(values, [2, 0, 1]), axis=0)  # shape (1, num_heads, qlen, klen)
        return values
