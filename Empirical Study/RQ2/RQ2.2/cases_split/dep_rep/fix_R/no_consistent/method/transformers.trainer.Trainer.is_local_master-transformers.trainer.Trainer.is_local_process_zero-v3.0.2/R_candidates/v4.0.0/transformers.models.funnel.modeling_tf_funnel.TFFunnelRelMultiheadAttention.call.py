    def call(self, query, key, value, attention_inputs, output_attentions=False, training=False):
        # query has shape batch_size x seq_len x d_model
        # key and value have shapes batch_size x context_len x d_model
        position_embeds, token_type_mat, attention_mask, cls_mask = attention_inputs

        batch_size, seq_len, _ = shape_list(query)
        context_len = key.shape[1]
        n_head, d_head = self.n_head, self.d_head

        # Shape batch_size x seq_len x n_head x d_head
        q_head = tf.reshape(self.q_head(query), [batch_size, seq_len, n_head, d_head])
        # Shapes batch_size x context_len x n_head x d_head
        k_head = tf.reshape(self.k_head(key), [batch_size, context_len, n_head, d_head])
        v_head = tf.reshape(self.v_head(value), [batch_size, context_len, n_head, d_head])

        q_head = q_head * self.scale
        # Shape n_head x d_head
        r_w_bias = self.r_w_bias * self.scale
        # Shapes batch_size x n_head x seq_len x context_len
        content_score = tf.einsum("bind,bjnd->bnij", q_head + r_w_bias, k_head)
        positional_attn = self.relative_positional_attention(position_embeds, q_head, context_len, cls_mask)
        token_type_attn = self.relative_token_type_attention(token_type_mat, q_head, cls_mask)

        # merge attention scores
        attn_score = content_score + positional_attn + token_type_attn

        # precision safe in case of mixed precision training
        dtype = attn_score.dtype
        if dtype != tf.float32:
            attn_score = tf.cast(attn_score, tf.float32)
        # perform masking
        if attention_mask is not None:
            attn_score = attn_score - INF * (1 - tf.cast(attention_mask[:, None, None], tf.float32))
        # attention probability
        attn_prob = tf.nn.softmax(attn_score, axis=-1)
        if dtype != tf.float32:
            attn_prob = tf.cast(attn_prob, dtype)
        attn_prob = self.attention_dropout(attn_prob, training=training)

        # attention output, shape batch_size x seq_len x n_head x d_head
        attn_vec = tf.einsum("bnij,bjnd->bind", attn_prob, v_head)

        # Shape shape batch_size x seq_len x d_model
        attn_out = self.post_proj(tf.reshape(attn_vec, [batch_size, seq_len, n_head * d_head]))
        attn_out = self.hidden_dropout(attn_out, training=training)

        output = self.layer_norm(query + attn_out)
        return (output, attn_prob) if output_attentions else (output,)
