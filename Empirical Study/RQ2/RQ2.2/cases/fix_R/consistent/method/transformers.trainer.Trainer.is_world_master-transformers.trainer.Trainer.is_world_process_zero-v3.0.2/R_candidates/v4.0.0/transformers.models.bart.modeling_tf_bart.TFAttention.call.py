    def call(
        self,
        query: tf.Tensor,
        key: tf.Tensor,
        key_padding_mask: Optional[tf.Tensor] = None,
        layer_state: Optional[Dict[str, tf.Tensor]] = None,
        attn_mask: Optional[Tensor] = None,
        training=False,
    ) -> Tuple[Tensor, Optional[Tensor]]:
        """
        Input shape: Time(SeqLen) x Batch x Channel

        Args:

            key_padding_mask (ByteTensor, optional): mask to exclude
                keys that are pads, of shape `(batch, src_len)`, where padding elements are indicated by 1s.
            attn_mask (ByteTensor, optional): typically used to
                implement causal attention, where the mask prevents the attention from looking forward in time
                (default: None).
        """
        static_kv = self.encoder_decoder_attention  # value=key=encoder_hidden_states,
        tgt_len, bsz, embed_dim = shape_list(query)
        assert (
            embed_dim == self.embed_dim
        ), f"query must be shaped {(tgt_len, bsz, self.embed_dim)} got {shape_list(query)}"
        # get here for encoder decoder cause of static_kv
        if layer_state is not None:  # get the last k and v for reuse
            saved_state = layer_state.get(self.cache_key, {})
            if "prev_key" in saved_state:
                # previous time steps are cached - no need to recompute key and value if they are static
                if static_kv:
                    key = None
        else:
            # this branch is hit by encoder
            saved_state = None

        # Project query key values using weights q_proj, k_proj, v_proj
        q = self.q_proj(query) * self.scaling
        if static_kv and key is None:  # cross-attention with cache
            k = v = None
        elif static_kv and key is not None:  # cross-attention no prev_key found in cache
            k = self.k_proj(key)
            v = self.v_proj(key)
        else:  # self-attention
            k = self.k_proj(query)
            v = self.v_proj(query)

        # Reshape
        q = self._shape(q, tgt_len, bsz)
        if k is not None:
            k = self._shape(k, -1, bsz)
            v = self._shape(v, -1, bsz)

        if saved_state:  # read from cache
            k, v = self._concat_saved_state(k, v, saved_state, static_kv, bsz)

        if layer_state is not None:  # Write to cache every decoder call
            cached_shape = (bsz, self.num_heads, -1, self.head_dim)  # bsz must be first for reorder_cache
            layer_state[self.cache_key] = dict(
                prev_key=tf.reshape(k, cached_shape), prev_value=tf.reshape(v, cached_shape)
            )

        # Compute multi-headed attention
        src_len = shape_list(k)[1]
        attn_weights = tf.matmul(q, k, transpose_b=True)  # shape (bsz * self.num_heads, tgt_len, src_len)

        if attn_mask is not None:
            assert attn_mask.dtype == tf.float32, f"expected dtype tf.float32 got {attn_mask.dtype}"
            attn_weights = tf.reshape(attn_weights, (bsz, self.num_heads, tgt_len, src_len)) + attn_mask
            attn_weights = tf.reshape(attn_weights, (bsz * self.num_heads, tgt_len, src_len))

        if key_padding_mask is not None:  # don't attend to padding symbols
            attn_weights: tf.Tensor = tf.reshape(attn_weights, (bsz, self.num_heads, tgt_len, src_len))
            if key_padding_mask.dtype == tf.bool:
                key_padding_mask = tf.cast(key_padding_mask, attn_weights.dtype) * -1e9
            extended_mask = tf.expand_dims(tf.expand_dims(key_padding_mask, 1), 2)
            attn_weights = attn_weights + extended_mask
            attn_weights = tf.reshape(attn_weights, (bsz * self.num_heads, tgt_len, src_len))

        attn_weights = tf.nn.softmax(attn_weights, axis=-1)
        attn_probs = tf.nn.dropout(attn_weights, rate=self.dropout if training else 0.0)

        attn_output = tf.matmul(attn_probs, v)  # shape: (bsz * self.num_heads, tgt_len, self.head_dim)
        attn_output = tf.transpose(attn_output, perm=(1, 0, 2))
        attn_output = tf.reshape(attn_output, (tgt_len, bsz, embed_dim))
        attn_output = self.out_proj(attn_output)
        attn_weights: tf.Tensor = tf.reshape(attn_weights, (bsz, self.num_heads, tgt_len, src_len))
        return attn_output, attn_weights
