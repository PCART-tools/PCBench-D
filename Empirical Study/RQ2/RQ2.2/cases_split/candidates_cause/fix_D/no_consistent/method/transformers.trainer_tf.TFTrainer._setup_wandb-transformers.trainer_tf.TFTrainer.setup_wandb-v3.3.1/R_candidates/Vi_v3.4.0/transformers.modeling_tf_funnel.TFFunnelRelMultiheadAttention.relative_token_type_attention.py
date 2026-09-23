    def relative_token_type_attention(self, token_type_mat, q_head, cls_mask=None):
        """ Relative attention score for the token_type_ids """
        if token_type_mat is None:
            return 0
        batch_size, seq_len, context_len = shape_list(token_type_mat)
        # q_head has shape batch_size x seq_len x n_head x d_head
        # Shape n_head x d_head
        r_s_bias = self.r_s_bias * self.scale

        # Shape batch_size x n_head x seq_len x 2
        token_type_bias = tf.einsum("bind,snd->bnis", q_head + r_s_bias, self.seg_embed)
        # Shape batch_size x n_head x seq_len x context_len
        new_shape = [batch_size, q_head.shape[2], seq_len, context_len]
        token_type_mat = tf.broadcast_to(token_type_mat[:, None], new_shape)
        # Shapes batch_size x n_head x seq_len
        diff_token_type, same_token_type = tf.split(token_type_bias, 2, axis=-1)
        # Shape batch_size x n_head x seq_len x context_len
        token_type_attn = tf.where(
            token_type_mat, tf.broadcast_to(same_token_type, new_shape), tf.broadcast_to(diff_token_type, new_shape)
        )

        if cls_mask is not None:
            token_type_attn *= cls_mask
        return token_type_attn
