    def _embedding(self, input_ids, position_ids, inputs_embeds, training=False):
        """
        Parameters:
            input_ids: tf.Tensor(bs, max_seq_length) The token ids to embed.

        Returns:
            tf.Tensor(bs, max_seq_length, dim) The embedded tokens (plus position embeddings, no token_type embeddings)
        """
        assert not (input_ids is None and inputs_embeds is None)

        if input_ids is not None:
            seq_length = shape_list(input_ids)[1]
        else:
            seq_length = shape_list(inputs_embeds)[1]

        if position_ids is None:
            position_ids = tf.range(seq_length, dtype=tf.int32)[tf.newaxis, :]

        if inputs_embeds is None:
            inputs_embeds = tf.gather(self.word_embeddings, input_ids)
        position_embeddings = tf.cast(
            self.position_embeddings(position_ids), inputs_embeds.dtype
        )  # (bs, max_seq_length, dim)

        embeddings = inputs_embeds + position_embeddings  # (bs, max_seq_length, dim)
        embeddings = self.LayerNorm(embeddings)  # (bs, max_seq_length, dim)
        embeddings = self.dropout(embeddings, training=training)  # (bs, max_seq_length, dim)
        return embeddings
