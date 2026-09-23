    def call(self, x, encoder_padding_mask, training=False):
        """
        Args:
            x (Tensor): input to the layer of shape `(seq_len, batch, embed_dim)`
            encoder_padding_mask (ByteTensor): binary ByteTensor of shape
                `(batch, src_len)` where padding elements are indicated by ``1``.
            for t_tgt, t_src is excluded (or masked out), =0 means it is
            included in attention

        Returns:
            encoded output of shape `(seq_len, batch, embed_dim)`
        """
        residual = x
        if self.normalize_before:
            x = self.self_attn_layer_norm(x)
        x, self_attn_weights = self.self_attn(query=x, key=x, key_padding_mask=encoder_padding_mask)
        assert shape_list(x) == shape_list(
            residual
        ), f"Self attn modified the shape of query {shape_list(residual)} to {shape_list(x)}"
        x = tf.nn.dropout(x, rate=self.dropout if training else 0)
        x = residual + x
        if not self.normalize_before:
            x = self.self_attn_layer_norm(x)

        residual = x
        if self.normalize_before:
            x = self.final_layer_norm(x)
        x = self.activation_fn(self.fc1(x))
        x = tf.nn.dropout(x, rate=self.activation_dropout if training else 0)
        x = self.fc2(x)
        x = tf.nn.dropout(x, rate=self.dropout if training else 0)
        x = residual + x
        if not self.normalize_before:
            x = self.final_layer_norm(x)

        return x, self_attn_weights
