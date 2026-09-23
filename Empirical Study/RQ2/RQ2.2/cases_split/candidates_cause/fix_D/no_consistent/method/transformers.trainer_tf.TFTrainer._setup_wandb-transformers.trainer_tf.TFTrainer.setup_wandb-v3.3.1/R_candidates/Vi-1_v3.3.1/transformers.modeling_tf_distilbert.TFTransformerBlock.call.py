    def call(self, x, attn_mask, head_mask, output_attentions, training=False):  # removed: src_enc=None, src_len=None
        """
        Parameters
        ----------
        x: tf.Tensor(bs, seq_length, dim)
        attn_mask: tf.Tensor(bs, seq_length)

        Outputs
        -------
        sa_weights: tf.Tensor(bs, n_heads, seq_length, seq_length)
            The attention weights
        ffn_output: tf.Tensor(bs, seq_length, dim)
            The output of the transformer block contextualization.
        """
        # Self-Attention
        sa_output = self.attention(x, x, x, attn_mask, head_mask, output_attentions, training=training)
        if output_attentions:
            sa_output, sa_weights = sa_output  # (bs, seq_length, dim), (bs, n_heads, seq_length, seq_length)
        else:  # To handle these `output_attentions` or `output_hidden_states` cases returning tuples
            # assert type(sa_output) == tuple
            sa_output = sa_output[0]
        sa_output = self.sa_layer_norm(sa_output + x)  # (bs, seq_length, dim)

        # Feed Forward Network
        ffn_output = self.ffn(sa_output, training=training)  # (bs, seq_length, dim)
        ffn_output = self.output_layer_norm(ffn_output + sa_output)  # (bs, seq_length, dim)

        output = (ffn_output,)
        if output_attentions:
            output = (sa_weights,) + output
        return output
