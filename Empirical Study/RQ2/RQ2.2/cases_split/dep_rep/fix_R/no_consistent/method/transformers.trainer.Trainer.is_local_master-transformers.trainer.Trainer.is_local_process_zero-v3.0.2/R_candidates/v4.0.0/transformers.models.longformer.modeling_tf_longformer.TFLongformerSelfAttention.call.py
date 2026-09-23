    def call(
        self,
        inputs,
        training=False,
    ):
        """
        LongformerSelfAttention expects `len(hidden_states)` to be multiple of `attention_window`. Padding to
        `attention_window` happens in LongformerModel.forward to avoid redoing the padding on each layer.

        The `attention_mask` is changed in `BertModel.forward` from 0, 1, 2 to -ve: no attention

              0: local attention
            +ve: global attention

        """
        # retrieve input args
        (
            hidden_states,
            attention_mask,
            is_index_masked,
            is_index_global_attn,
            is_global_attn,
        ) = inputs

        # project hidden states
        query_vectors = self.query(hidden_states)
        key_vectors = self.key(hidden_states)
        value_vectors = self.value(hidden_states)
        batch_size, seq_len, embed_dim = shape_list(hidden_states)

        tf.debugging.assert_equal(
            embed_dim,
            self.embed_dim,
            message=f"hidden_states should have embed_dim = {self.embed_dim}, but has {embed_dim}",
        )

        # normalize query
        query_vectors /= tf.math.sqrt(tf.constant(self.head_dim, dtype=tf.dtypes.float32))
        query_vectors = tf.reshape(query_vectors, (batch_size, seq_len, self.num_heads, self.head_dim))
        key_vectors = tf.reshape(key_vectors, (batch_size, seq_len, self.num_heads, self.head_dim))

        # attn_probs = (batch_size, seq_len, num_heads, window*2+1)
        attn_scores = self._sliding_chunks_query_key_matmul(
            query_vectors, key_vectors, self.one_sided_attn_window_size
        )

        # diagonal mask with zeros everywhere and -inf inplace of padding
        diagonal_mask = self._sliding_chunks_query_key_matmul(
            tf.ones(shape_list(attention_mask), dtype=tf.float32),
            attention_mask,
            self.one_sided_attn_window_size,
        )

        # pad local attention probs
        attn_scores += diagonal_mask

        tf.debugging.assert_equal(
            shape_list(attn_scores),
            [batch_size, seq_len, self.num_heads, self.one_sided_attn_window_size * 2 + 1],
            message=f"attn_probs should be of size ({batch_size}, {seq_len}, {self.num_heads}, {self.one_sided_attn_window_size * 2 + 1}), but is of size {shape_list(attn_scores)}",
        )

        # compute global attn indices required through out forward fn
        (
            max_num_global_attn_indices,
            is_index_global_attn_nonzero,
            is_local_index_global_attn_nonzero,
            is_local_index_no_global_attn_nonzero,
        ) = self._get_global_attn_indices(is_index_global_attn)

        # this function is only relevant for global attention
        attn_scores = tf.cond(
            is_global_attn,
            lambda: self._concat_with_global_key_attn_probs(
                attn_scores=attn_scores,
                query_vectors=query_vectors,
                key_vectors=key_vectors,
                max_num_global_attn_indices=max_num_global_attn_indices,
                is_index_global_attn_nonzero=is_index_global_attn_nonzero,
                is_local_index_global_attn_nonzero=is_local_index_global_attn_nonzero,
                is_local_index_no_global_attn_nonzero=is_local_index_no_global_attn_nonzero,
            ),
            lambda: attn_scores,
        )

        attn_probs = tf.nn.softmax(attn_scores, axis=-1)

        # softmax sometimes inserts NaN if all positions are masked, replace them with 0
        attn_probs = tf.where(
            tf.broadcast_to(is_index_masked[:, :, None, None], shape_list(attn_probs)),
            0.0,
            attn_probs,
        )

        # apply dropout
        attn_probs = self.dropout(attn_probs, training=training)
        value_vectors = tf.reshape(value_vectors, (batch_size, seq_len, self.num_heads, self.head_dim))

        # if global attention, compute sum of global and local attn
        attn_output = tf.cond(
            is_global_attn,
            lambda: self._compute_attn_output_with_global_indices(
                value_vectors=value_vectors,
                attn_probs=attn_probs,
                max_num_global_attn_indices=max_num_global_attn_indices,
                is_index_global_attn_nonzero=is_index_global_attn_nonzero,
                is_local_index_global_attn_nonzero=is_local_index_global_attn_nonzero,
            ),
            lambda: self._sliding_chunks_matmul_attn_probs_value(
                attn_probs, value_vectors, self.one_sided_attn_window_size
            ),
        )

        tf.debugging.assert_equal(
            shape_list(attn_output),
            [batch_size, seq_len, self.num_heads, self.head_dim],
            message="Unexpected size",
        )

        attn_output = tf.reshape(attn_output, (batch_size, seq_len, embed_dim))

        # compute value for global attention and overwrite to attention output
        # TODO: remove the redundant computation
        attn_output, global_attn_probs = tf.cond(
            is_global_attn,
            lambda: self._compute_global_attn_output_from_hidden(
                attn_output=attn_output,
                hidden_states=hidden_states,
                max_num_global_attn_indices=max_num_global_attn_indices,
                is_local_index_global_attn_nonzero=is_local_index_global_attn_nonzero,
                is_index_global_attn_nonzero=is_index_global_attn_nonzero,
                is_local_index_no_global_attn_nonzero=is_local_index_no_global_attn_nonzero,
                is_index_masked=is_index_masked,
                training=training,
            ),
            lambda: (attn_output, tf.zeros((batch_size, self.num_heads, max_num_global_attn_indices, seq_len))),
        )

        # make sure that local attention probabilities are set to 0 for indices of global attn
        attn_probs = tf.where(
            tf.broadcast_to(is_index_global_attn[:, :, None, None], shape_list(attn_probs)),
            tf.zeros(shape_list(attn_probs), dtype=tf.dtypes.float32),
            attn_probs,
        )

        outputs = (attn_output, attn_probs, global_attn_probs)

        return outputs
