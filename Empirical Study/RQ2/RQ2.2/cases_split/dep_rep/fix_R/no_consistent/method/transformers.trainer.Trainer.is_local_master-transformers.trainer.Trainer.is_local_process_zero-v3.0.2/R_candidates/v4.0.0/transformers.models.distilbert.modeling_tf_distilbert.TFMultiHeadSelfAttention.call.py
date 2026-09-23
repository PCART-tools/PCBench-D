    def call(self, query, key, value, mask, head_mask, output_attentions, training=False):
        """
        Parameters:
            query: tf.Tensor(bs, seq_length, dim)
            key: tf.Tensor(bs, seq_length, dim)
            value: tf.Tensor(bs, seq_length, dim)
            mask: tf.Tensor(bs, seq_length)

        Returns:
            weights: tf.Tensor(bs, n_heads, seq_length, seq_length) Attention weights context: tf.Tensor(bs,
            seq_length, dim) Contextualized layer. Optional: only if `output_attentions=True`
        """
        bs, q_length, dim = shape_list(query)
        k_length = shape_list(key)[1]
        # assert dim == self.dim, 'Dimensions do not match: %s input vs %s configured' % (dim, self.dim)
        # assert key.size() == value.size()
        dim_per_head = tf.math.divide(self.dim, self.n_heads)
        dim_per_head = tf.cast(dim_per_head, dtype=tf.int32)
        mask_reshape = [bs, 1, 1, k_length]

        def shape(x):
            """ separate heads """
            return tf.transpose(tf.reshape(x, (bs, -1, self.n_heads, dim_per_head)), perm=(0, 2, 1, 3))

        def unshape(x):
            """ group heads """
            return tf.reshape(tf.transpose(x, perm=(0, 2, 1, 3)), (bs, -1, self.n_heads * dim_per_head))

        q = shape(self.q_lin(query))  # (bs, n_heads, q_length, dim_per_head)
        k = shape(self.k_lin(key))  # (bs, n_heads, k_length, dim_per_head)
        v = shape(self.v_lin(value))  # (bs, n_heads, k_length, dim_per_head)
        q = tf.cast(q, dtype=tf.float32)
        q = tf.multiply(q, tf.math.rsqrt(tf.cast(dim_per_head, dtype=tf.float32)))
        k = tf.cast(k, dtype=q.dtype)
        scores = tf.matmul(q, k, transpose_b=True)  # (bs, n_heads, q_length, k_length)
        mask = tf.reshape(mask, mask_reshape)  # (bs, n_heads, qlen, klen)
        # scores.masked_fill_(mask, -float('inf'))            # (bs, n_heads, q_length, k_length)

        mask = tf.cast(mask, dtype=scores.dtype)
        scores = scores - 1e30 * (1.0 - mask)
        weights = tf.nn.softmax(scores, axis=-1)  # (bs, n_heads, qlen, klen)
        weights = self.dropout(weights, training=training)  # (bs, n_heads, qlen, klen)

        # Mask heads if we want to
        if head_mask is not None:
            weights = weights * head_mask

        context = tf.matmul(weights, v)  # (bs, n_heads, qlen, dim_per_head)
        context = unshape(context)  # (bs, q_length, dim)
        context = self.out_lin(context)  # (bs, q_length, dim)

        if output_attentions:
            return (context, weights)
        else:
            return (context,)
